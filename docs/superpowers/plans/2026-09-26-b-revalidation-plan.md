# B Revalidation Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a documented, standard-library-only B revalidation package that runs rebuild/test/recheck against a candidate workspace and emits auditable accept/reject evidence without claiming unprovided real execution results.

**Architecture:** A small Python module owns request validation, ordered stage execution, recheck-report inspection, and JSON report generation. The CLI is a thin adapter over that module; documentation and examples define the handoff boundary with the existing v0.2 contract and B2 receipt. Tests use temporary workspaces and Python child scripts to exercise the runner without introducing product dependencies.

**Tech Stack:** Python 3.10+ standard library (`argparse`, `dataclasses`, `json`, `pathlib`, `subprocess`, `tempfile`, `unittest`), Markdown, JSON.

**Spec:** `docs/superpowers/specs/2026-09-26-b-revalidation-design.md`

## Global Constraints

- Keep the root `ab-job-contract.schema.json` and `接口定义文档_v0.2.md` unchanged; B supplements the contract and does not redefine it.
- Use `schema_version: "2.0"`, full 40-character lowercase hexadecimal `base_commit` and `candidate_commit`, non-empty `finding_ids`, and a non-empty `configuration_id`.
- Execute stages in order: optional `clean`, required `build`, required `test`, required `recheck`; stop after the first failed or timed-out stage.
- A candidate is `ACCEPTED` only when build, test, and recheck exit with code 0 and no selected finding remains.
- Any failed validation or execution must be `REJECTED`; execution failures use `REPAIR_3001`, request failures use `VALIDATION_1001`; never report a failed candidate as successful.
- Keep log paths and handoff fields repository-relative; do not emit machine absolute paths as Artifact handoff values.
- Add no third-party runtime or test dependency; use `python -m unittest`.
- Examples are placeholders and must say so; no example may be presented as real rebuild/test/recheck evidence.

## Review Focus

- A successful recheck process that still reports an unrelated finding must be accepted only if the selected finding IDs are gone; test that only selected IDs control the decision.
- A failed build or test must prevent later stages from running; test sentinel files for skipped stages.
- A malformed or missing recheck report after exit code 0 must be rejected with a useful stage error; test both JSON parse and shape failures.
- A command timeout must stop the stage and preserve a rejected report with timeout evidence; test the timeout path.
- Path traversal or absolute recheck-report paths must be rejected before commands run; test request validation and the no-execution guarantee.

---

### Task 1: Build the revalidation engine with red-green tests

**Files:**
- Create: `B-重新验证/tests/test_revalidate.py`
- Create: `B-重新验证/tools/revalidate.py`

**Interfaces:**
- Consumes: A Python mapping with `schema_version`, `base_commit`, `candidate_commit`, `configuration_id`, `finding_ids`, `commands`, `recheck_report`, and `timeout_seconds`; a candidate workspace `pathlib.Path`.
- Produces: `validate_request(request: Mapping[str, object]) -> None`, `run_verification(request: Mapping[str, object], workspace: Path, output_path: Path) -> dict[str, object]`, and `main(argv: Sequence[str] | None = None) -> int`.
- Report contract: `verification_status`, commit/configuration/finding fields, `validation.clean/build/test/recheck`, `remaining_selected_findings`, `error`, and UTC `generated_at`; stage records contain `success`, `exit_code`, `duration_ms`, `log_path` and optional `skipped`/`timed_out` fields.

- [ ] **Step 1: Write failing tests for request validation and the success path**

  Add `unittest` cases that create a temporary workspace and tiny Python stage scripts. Assert that invalid SHA, empty `finding_ids`, blank required commands, absolute/traversing `recheck_report`, and non-positive timeout raise a request-validation error. Add a success case whose recheck script writes a valid `findings` array without the selected finding; assert `ACCEPTED`, all required stages succeed, `remaining_selected_findings == []`, report JSON is written, and every `log_path` is relative.

- [ ] **Step 2: Run the focused tests to verify they fail for the missing engine**

  Run: `python -m unittest discover -s B-重新验证/tests -p "test_*.py" -v`

  Expected: FAIL because `B-重新验证/tools/revalidate.py` does not yet provide the requested functions.

- [ ] **Step 3: Implement request validation and ordered stage execution**

  In `B-重新验证/tools/revalidate.py`, implement a `RequestValidationError` carrying `code`, `message`, and optional `field`; validate exact version, commit format, IDs, command presence, safe relative recheck path, and positive timeout. Implement a stage runner using `subprocess.run(..., shell=True, cwd=workspace, capture_output=True, text=True, timeout=...)`; write stdout/stderr to `b-evidence/<stage>.log`, measure duration, mark timeouts, and return relative log paths. Stop at the first failed stage and mark later stages skipped.

- [ ] **Step 4: Implement recheck inspection and report generation**

  Load the configured recheck JSON only after the recheck command succeeds. Require an object with an array `findings`; require each finding to have a string `finding_id`; compute `remaining_selected_findings` by intersection with the requested IDs. Return `ACCEPTED` only when build/test/recheck succeeded and the intersection is empty. Use `REPAIR_3001` for stage/report/finding failures and `VALIDATION_1001` for request failures; write a report even for rejected execution, while keeping validation failures from starting any command.

- [ ] **Step 5: Run the focused tests to verify the engine passes the initial contract**

  Run: `python -m unittest discover -s B-重新验证/tests -p "test_*.py" -v`

  Expected: PASS for validation and success-path tests.

- [ ] **Step 6: Commit the engine baseline**

  ```powershell
  git add B-重新验证/tests/test_revalidate.py B-重新验证/tools/revalidate.py
  git commit -m "feat: add B revalidation engine"
  ```

### Task 2: Cover failure modes and add the CLI contract

**Files:**
- Modify: `B-重新验证/tests/test_revalidate.py`
- Modify: `B-重新验证/tools/revalidate.py`

**Interfaces:**
- Consumes: Task 1 `run_verification` and report shape.
- Produces: CLI flags `--request`, `--workspace`, and `--output`; exit code `0` for `ACCEPTED`, `1` for `REJECTED`, and `2` for request/file errors; rejected reports with stage-specific evidence.

- [ ] **Step 1: Write failing tests for build/test/recheck failures, malformed reports, timeouts, and CLI exit codes**

  Add tests for: build non-zero stopping test/recheck; test non-zero stopping recheck; recheck success with a selected finding remaining; invalid JSON; valid JSON with invalid `findings`; command timeout; and CLI success/rejection return codes using temporary request/report files. Use sentinel files to prove skipped stages did not execute.

- [ ] **Step 2: Run the failure-mode tests to verify they fail before the new behavior exists**

  Run: `python -m unittest discover -s B-重新验证/tests -p "test_*.py" -v`

  Expected: FAIL in the newly added failure-mode assertions.

- [ ] **Step 3: Implement failure reporting and CLI parsing**

  Extend the engine to emit `skipped` stage records after an earlier failure, preserve timeout metadata, distinguish malformed recheck content from command failure, and serialize reports with stable UTF-8 JSON. Add `argparse` handling for the three required flags, load the request JSON, ensure workspace and output paths are usable, call `run_verification`, print a concise status line, and return the specified exit code without printing absolute paths into the JSON report.

- [ ] **Step 4: Run the complete Python test suite**

  Run: `python -m unittest discover -s B-重新验证/tests -p "test_*.py" -v`

  Expected: All tests pass, including the five review-focus failure classes.

- [ ] **Step 5: Commit the CLI and failure-mode coverage**

  ```powershell
  git add B-重新验证/tests/test_revalidate.py B-重新验证/tools/revalidate.py
  git commit -m "test: cover B revalidation failure modes"
  ```

### Task 3: Add the B handoff documentation and placeholder evidence

**Files:**
- Create: `B-重新验证/README.md`
- Create: `B-重新验证/docs/revalidation.md`
- Create: `B-重新验证/docs/instance-values.md`
- Create: `B-重新验证/examples/revalidation-request.example.json`
- Create: `B-重新验证/examples/revalidation-report-succeeded.example.json`
- Create: `B-重新验证/examples/revalidation-report-rejected.example.json`
- Create: `B-重新验证/AI_USAGE.md`

**Interfaces:**
- Consumes: Task 1/2 CLI flags and report fields; existing `B2-MDFixer-MD交接/docs/md-reception.md`, `接口定义文档_v0.2.md`, and `A-BuildChecker-EChecker-接口文档/ADR-002-artifact-storage-and-access.md`.
- Produces: A copyable B package explaining inputs, phase order, acceptance/rejection, Artifact URI mapping, evidence ownership, real-value checklist, and placeholder examples.

- [ ] **Step 1: Write the README and detailed revalidation procedure**

  Document B’s role, the boundary after B2 accepts a report, the distinction between applying a patch and verifying an already-applied candidate, the exact CLI invocation, phase stop conditions, `REPAIR_3001` behavior, final B+B2 acceptance, and the fact that no real run is claimed in the examples.

- [ ] **Step 2: Write the instance-values checklist and placeholder JSON samples**

  Add a table for pair/job IDs, repository URL, `base_commit`, `candidate_commit`, configuration, commands, candidate workspace, Artifact URIs, SHA-256 values, operator and timestamps. Add valid structural request, accepted report, and rejected report samples using obvious placeholders and a top-level notice that they are not execution evidence. Keep the accepted sample’s remaining selected findings empty and the rejected sample’s error code `REPAIR_3001`.

- [ ] **Step 3: Record AI usage and cross-document references**

  Add `AI_USAGE.md` with the prompt summary, Codex’s proposed B boundary, human decisions, files affected, and validation commands. Link the root contract, B2 receipt, A group artifact rules, and the B design/plan without copying or changing their definitions.

- [ ] **Step 4: Run documentation and JSON consistency checks**

  Run:

  ```powershell
  python -m json.tool B-重新验证/examples/revalidation-request.example.json > $null
  python -m json.tool B-重新验证/examples/revalidation-report-succeeded.example.json > $null
  python -m json.tool B-重新验证/examples/revalidation-report-rejected.example.json > $null
  rg -n "真实|real|placeholder|占位|待确认|REPAIR_3001|ACCEPTED|REJECTED" B-重新验证
  git diff --check
  ```

  Expected: all JSON commands exit 0; documentation explicitly marks examples as placeholders, contains both decision states and the failure code, and `git diff --check` reports no whitespace errors.

- [ ] **Step 5: Commit the B documentation package**

  ```powershell
  git add B-重新验证/README.md B-重新验证/docs B-重新验证/examples B-重新验证/AI_USAGE.md
  git commit -m "docs: add B revalidation handoff package"
  ```

### Task 4: Perform whole-branch verification and handoff

**Files:**
- Modify only if verification finds a defect in Task 1–3 files.

**Interfaces:**
- Consumes: The complete B package and the approved design.
- Produces: A clean, test-backed branch ready to push, with no claim of real rebuild/test/recheck execution because no real project inputs were supplied.

- [ ] **Step 1: Run the complete automated test suite**

  Run: `python -m unittest discover -s B-重新验证/tests -p "test_*.py" -v`

  Expected: all tests pass.

- [ ] **Step 2: Run the CLI against a temporary synthetic candidate**

  Create a temporary request/workspace using the same stage scripts as the tests, run the documented CLI, and inspect the emitted report. Expected: process exit code `0`, `verification_status` `ACCEPTED`, selected findings empty, and log paths relative to the workspace.

- [ ] **Step 3: Run repository-level consistency checks**

  Run `git diff --check`, parse all three example JSON files with `python -m json.tool`, and inspect `git status --short --branch`, `git diff --stat main...HEAD`, and `git log --oneline main..HEAD`.

  Expected: no whitespace errors, all samples parse, only the intended B package and supporting commits are present, and no unrelated user changes are modified.

- [ ] **Step 4: Commit any verification-only fix with its regression test**

  If a defect appears, write the reproducing test first, observe failure, make the smallest fix, rerun the complete suite, and commit with a focused message. If no defect appears, make no extra commit.

- [ ] **Step 5: Push the completed branch to the provided GitHub repository**

  ```powershell
  git push -u origin codex/b-revalidation
  ```

  Expected: the remote accepts the branch. Report the branch name, final commit SHA, verification commands and the limitation that no real candidate rebuild/test/recheck was available in this E2 documentation repository.

## Plan Self-Review

- Spec coverage: Task 1 covers validation, ordered execution and report semantics; Task 2 covers all specified failure paths and the CLI; Task 3 covers every documented deliverable and cross-document boundary; Task 4 covers final evidence and push.
- Step scan: every implementation task starts with a failing test; documentation and verification tasks use checkable commands and expected outcomes.
- Type/interface consistency: Task 1 defines `validate_request`, `run_verification`, `main`, stage/report fields and error codes; Task 2 consumes those exact names and fields; Task 3 documents the same CLI and report shape.
- Review focus coverage: success/selected finding logic is in Task 1; stop-on-failure, malformed reports, timeouts and path safety are in Task 2; whole-branch CLI and relative-path evidence are rechecked in Task 4.
- Proportion: the plan adds one small runner, one test module, and a focused handoff package; it does not introduce a service, container runtime, or dependency graph implementation.
