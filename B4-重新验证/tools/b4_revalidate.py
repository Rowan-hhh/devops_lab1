"""Run the B4 rebuild, test, and recheck verification flow."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Mapping, Sequence


COMMIT_PATTERN = set("0123456789abcdef")
REPAIR_FAILURE = "REPAIR_3001"
VALIDATION_FAILURE = "VALIDATION_1001"


class RequestValidationError(ValueError):
    """Raised when a B4 verification request cannot be executed safely."""

    def __init__(self, message: str, field: str | None = None):
        self.code = VALIDATION_FAILURE
        self.message = message
        self.field = field
        super().__init__(message)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _is_full_commit(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and value == value.lower()
        and set(value) <= COMMIT_PATTERN
    )


def _safe_relative_path(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RequestValidationError("path must be a non-empty string", field)
    posix_path = PurePosixPath(value)
    windows_path = PureWindowsPath(value)
    if posix_path.is_absolute() or windows_path.is_absolute() or windows_path.drive:
        raise RequestValidationError("path must be repository-relative", field)
    if ".." in posix_path.parts or ".." in windows_path.parts:
        raise RequestValidationError("path must not traverse parent directories", field)
    return value


def validate_request(request: Mapping[str, object]) -> None:
    """Validate the B4 request before any command is started."""

    if not isinstance(request, Mapping):
        raise RequestValidationError("request must be a JSON object")
    if request.get("schema_version") != "2.0":
        raise RequestValidationError("schema_version must be '2.0'", "schema_version")

    for field in ("base_commit", "candidate_commit"):
        if not _is_full_commit(request.get(field)):
            raise RequestValidationError(
                f"{field} must be a 40-character lowercase hexadecimal SHA", field
            )

    configuration_id = request.get("configuration_id")
    if not isinstance(configuration_id, str) or not configuration_id.strip():
        raise RequestValidationError(
            "configuration_id must be a non-empty string", "configuration_id"
        )

    finding_ids = request.get("finding_ids")
    if (
        not isinstance(finding_ids, list)
        or not finding_ids
        or any(not isinstance(item, str) or not item.strip() for item in finding_ids)
        or len(set(finding_ids)) != len(finding_ids)
    ):
        raise RequestValidationError(
            "finding_ids must be a non-empty list of unique strings", "finding_ids"
        )

    commands = request.get("commands")
    if not isinstance(commands, Mapping):
        raise RequestValidationError("commands must be an object", "commands")
    for field in ("build", "test", "recheck"):
        command = commands.get(field)
        if not isinstance(command, str) or not command.strip():
            raise RequestValidationError(
                f"commands.{field} must be a non-empty string", f"commands.{field}"
            )
    clean = commands.get("clean", "")
    if clean is not None and not isinstance(clean, str):
        raise RequestValidationError("commands.clean must be a string", "commands.clean")

    _safe_relative_path(request.get("recheck_report"), "recheck_report")

    timeout = request.get("timeout_seconds")
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
        raise RequestValidationError(
            "timeout_seconds must be a positive number", "timeout_seconds"
        )


def _relative_to_workspace(path: Path, workspace: Path) -> str:
    return path.resolve().relative_to(workspace.resolve()).as_posix()


def _stage_record_skipped(reason: str, success: bool = False) -> dict[str, object]:
    return {
        "success": success,
        "exit_code": 0 if success else None,
        "duration_ms": 0,
        "log_path": None,
        "skipped": True,
        "reason": reason,
    }


def _stage_record(
    command: str,
    stage: str,
    workspace: Path,
    evidence_dir: Path,
    timeout_seconds: float,
) -> dict[str, object]:
    log_path = evidence_dir / f"{stage}.log"
    started = time.monotonic()
    timed_out = False
    error_message: str | None = None
    exit_code: int | None = None
    stdout = ""
    stderr = ""
    try:
        completed = subprocess.run(
            command,
            cwd=workspace,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        exit_code = completed.returncode
        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        error_message = f"{stage} timed out after {timeout_seconds:g} seconds"
    except OSError as exc:
        error_message = f"{stage} could not start: {exc}"

    duration_ms = int((time.monotonic() - started) * 1000)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_text = f"$ {command}\n\n[stdout]\n{stdout}\n[stderr]\n{stderr}"
    if error_message:
        log_text += f"\n[error]\n{error_message}\n"
    log_path.write_text(log_text, encoding="utf-8")

    record: dict[str, object] = {
        "success": not timed_out and exit_code == 0,
        "exit_code": exit_code,
        "duration_ms": duration_ms,
        "log_path": _relative_to_workspace(log_path, workspace),
    }
    if timed_out:
        record["timed_out"] = True
    if error_message:
        record["error"] = error_message
    return record


def _write_report(report: dict[str, object], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _base_report(request: Mapping[str, object]) -> dict[str, object]:
    return {
        "schema_version": "2.0",
        "verification_status": "REJECTED",
        "base_commit": request.get("base_commit"),
        "candidate_commit": request.get("candidate_commit"),
        "configuration_id": request.get("configuration_id"),
        "finding_ids": request.get("finding_ids", []),
        "validation": {},
        "remaining_selected_findings": [],
        "error": None,
        "generated_at": _utc_now(),
    }


def _failure(message: str, stage: str | None = None) -> dict[str, object]:
    error: dict[str, object] = {"code": REPAIR_FAILURE, "message": message}
    if stage:
        error["stage"] = stage
    return error


def _load_recheck_report(
    request: Mapping[str, object], workspace: Path
) -> tuple[list[str], str | None]:
    report_relative = _safe_relative_path(request["recheck_report"], "recheck_report")
    report_path = (workspace / Path(report_relative)).resolve()
    try:
        report_path.relative_to(workspace.resolve())
    except ValueError:
        return [], "recheck_report resolves outside the candidate workspace"
    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [], f"recheck report not found: {report_relative}"
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [], f"recheck report could not be read: {exc}"
    if not isinstance(payload, dict) or not isinstance(payload.get("findings"), list):
        return [], "recheck report must be an object with a findings array"
    finding_ids: list[str] = []
    for index, finding in enumerate(payload["findings"]):
        if not isinstance(finding, dict) or not isinstance(finding.get("finding_id"), str):
            return [], f"recheck finding at index {index} lacks a string finding_id"
        finding_ids.append(finding["finding_id"])
    return finding_ids, None


def run_verification(
    request: Mapping[str, object], workspace: Path, output_path: Path
) -> dict[str, object]:
    """Run the configured B4 stages and write an auditable JSON report."""

    validate_request(request)
    workspace = Path(workspace).resolve()
    output_path = Path(output_path)
    if not output_path.is_absolute():
        output_path = workspace / output_path
    if not workspace.is_dir():
        raise ValueError(f"workspace does not exist: {workspace}")

    report = _base_report(request)
    evidence_dir = workspace / "b4-evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    commands = request["commands"]
    timeout_seconds = float(request["timeout_seconds"])
    stages = ("clean", "build", "test", "recheck")
    stopped = False

    for stage in stages:
        command = commands.get(stage, "")
        if not command or not str(command).strip():
            report["validation"][stage] = _stage_record_skipped(
                "not configured", success=True
            )
            continue
        if stopped:
            report["validation"][stage] = _stage_record_skipped(
                "stopped after a previous stage failed"
            )
            continue
        stage_result = _stage_record(
            str(command), stage, workspace, evidence_dir, timeout_seconds
        )
        report["validation"][stage] = stage_result
        if not stage_result["success"]:
            report["error"] = _failure(
                stage_result.get("error")
                or f"{stage} exited with code {stage_result.get('exit_code')}",
                stage,
            )
            stopped = True
            continue
        if stage == "recheck":
            actual_findings, recheck_error = _load_recheck_report(request, workspace)
            if recheck_error:
                report["error"] = _failure(recheck_error, "recheck")
                stopped = True
            else:
                selected = set(request["finding_ids"])
                report["remaining_selected_findings"] = [
                    finding_id for finding_id in request["finding_ids"] if finding_id in actual_findings
                ]
                if report["remaining_selected_findings"]:
                    report["error"] = _failure(
                        "selected finding(s) remain after recheck", "recheck"
                    )

    if report["error"] is None:
        report["verification_status"] = "ACCEPTED"
    _write_report(report, output_path)
    return report


def _validation_report(request: object, error: RequestValidationError) -> dict[str, object]:
    report = _base_report(request if isinstance(request, Mapping) else {})
    report["error"] = {
        "code": error.code,
        "message": error.message,
    }
    if error.field:
        report["error"]["field"] = error.field
    return report


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point; detailed CLI error handling is extended in Task 2."""

    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        request = json.loads(args.request.read_text(encoding="utf-8"))
        report = run_verification(request, args.workspace, args.output)
    except RequestValidationError as exc:
        report = _validation_report({}, exc)
        _write_report(report, args.output)
        return 2
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        report = _validation_report({}, RequestValidationError(str(exc)))
        _write_report(report, args.output)
        return 2
    except ValueError as exc:
        report = _validation_report({}, RequestValidationError(str(exc)))
        _write_report(report, args.output)
        return 2
    print(report["verification_status"])
    return 0 if report["verification_status"] == "ACCEPTED" else 1


if __name__ == "__main__":
    sys.exit(main())
