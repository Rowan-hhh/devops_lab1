import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from b4_revalidate import (  # noqa: E402
    RequestValidationError,
    main,
    run_verification,
    validate_request,
)


class RevalidationEngineTests(unittest.TestCase):
    def make_request(self):
        return {
            "schema_version": "2.0",
            "base_commit": "1" * 40,
            "candidate_commit": "2" * 40,
            "configuration_id": "cc-MODE0",
            "finding_ids": ["finding-md-001"],
            "commands": {
                "clean": "",
                "build": "build.py",
                "test": "test.py",
                "recheck": "recheck.py",
            },
            "recheck_report": "evidence/recheck.json",
            "timeout_seconds": 5,
        }

    def write_script(self, workspace, name, body):
        path = workspace / name
        path.write_text(body, encoding="utf-8")
        return path

    def test_validate_request_rejects_invalid_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            cases = [
                ("base_commit", "not-a-sha"),
                ("finding_ids", []),
                ("commands", {"build": "", "test": "test.py", "recheck": "recheck.py"}),
                ("recheck_report", str(workspace / "absolute.json")),
                ("recheck_report", "../outside.json"),
                ("timeout_seconds", 0),
            ]
            for field, value in cases:
                with self.subTest(field=field, value=value):
                    request = self.make_request()
                    if field == "commands":
                        request["commands"] = value
                    else:
                        request[field] = value
                    with self.assertRaises(RequestValidationError):
                        validate_request(request)

    def test_success_accepts_when_selected_finding_is_gone(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            self.write_script(
                workspace,
                "build.py",
                "from pathlib import Path\nPath('build-ran').write_text('ok', encoding='utf-8')\n",
            )
            self.write_script(
                workspace,
                "test.py",
                "from pathlib import Path\nPath('test-ran').write_text('ok', encoding='utf-8')\n",
            )
            self.write_script(
                workspace,
                "recheck.py",
                "import json\nfrom pathlib import Path\nPath('evidence').mkdir(exist_ok=True)\nPath('evidence/recheck.json').write_text(json.dumps({'findings': [{'finding_id': 'unrelated-finding'}]}), encoding='utf-8')\n",
            )
            request = self.make_request()
            request["commands"] = {
                "build": f'"{sys.executable}" build.py',
                "test": f'"{sys.executable}" test.py',
                "recheck": f'"{sys.executable}" recheck.py',
            }
            output_path = workspace / "verification.json"

            report = run_verification(request, workspace, output_path)

            self.assertEqual(report["verification_status"], "ACCEPTED")
            self.assertEqual(report["remaining_selected_findings"], [])
            self.assertIsNone(report["error"])
            self.assertTrue(output_path.exists())
            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), report)
            for stage_name in ("build", "test", "recheck"):
                stage = report["validation"][stage_name]
                self.assertTrue(stage["success"])
                self.assertEqual(stage["exit_code"], 0)
                self.assertFalse(Path(stage["log_path"]).is_absolute())
                self.assertTrue((workspace / stage["log_path"]).exists())

    def test_build_failure_stops_later_stages(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            self.write_script(
                workspace,
                "build.py",
                "from pathlib import Path\nPath('build-ran').write_text('yes', encoding='utf-8')\nraise SystemExit(3)\n",
            )
            self.write_script(
                workspace,
                "test.py",
                "from pathlib import Path\nPath('test-ran').write_text('yes', encoding='utf-8')\n",
            )
            self.write_script(
                workspace,
                "recheck.py",
                "from pathlib import Path\nPath('recheck-ran').write_text('yes', encoding='utf-8')\n",
            )
            request = self.make_request()
            request["commands"] = {
                "build": f'"{sys.executable}" build.py',
                "test": f'"{sys.executable}" test.py',
                "recheck": f'"{sys.executable}" recheck.py',
            }

            report = run_verification(request, workspace, workspace / "report.json")

            self.assertEqual(report["verification_status"], "REJECTED")
            self.assertEqual(report["error"]["code"], "REPAIR_3001")
            self.assertEqual(report["validation"]["build"]["exit_code"], 3)
            self.assertTrue(report["validation"]["test"]["skipped"])
            self.assertTrue(report["validation"]["recheck"]["skipped"])
            self.assertFalse((workspace / "test-ran").exists())
            self.assertFalse((workspace / "recheck-ran").exists())

    def test_test_failure_stops_recheck(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            self.write_script(workspace, "build.py", "raise SystemExit(0)\n")
            self.write_script(
                workspace,
                "test.py",
                "from pathlib import Path\nPath('test-ran').write_text('yes', encoding='utf-8')\nraise SystemExit(4)\n",
            )
            self.write_script(
                workspace,
                "recheck.py",
                "from pathlib import Path\nPath('recheck-ran').write_text('yes', encoding='utf-8')\n",
            )
            request = self.make_request()
            request["commands"] = {
                "build": f'"{sys.executable}" build.py',
                "test": f'"{sys.executable}" test.py',
                "recheck": f'"{sys.executable}" recheck.py',
            }

            report = run_verification(request, workspace, workspace / "report.json")

            self.assertEqual(report["verification_status"], "REJECTED")
            self.assertEqual(report["validation"]["test"]["exit_code"], 4)
            self.assertTrue(report["validation"]["recheck"]["skipped"])
            self.assertFalse((workspace / "recheck-ran").exists())

    def test_remaining_selected_finding_rejects_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            self.write_script(workspace, "build.py", "raise SystemExit(0)\n")
            self.write_script(workspace, "test.py", "raise SystemExit(0)\n")
            self.write_script(
                workspace,
                "recheck.py",
                "import json\nfrom pathlib import Path\nPath('evidence').mkdir(exist_ok=True)\nPath('evidence/recheck.json').write_text(json.dumps({'findings': [{'finding_id': 'finding-md-001'}, {'finding_id': 'unrelated-finding'}]}), encoding='utf-8')\n",
            )
            request = self.make_request()
            request["commands"] = {
                "build": f'"{sys.executable}" build.py',
                "test": f'"{sys.executable}" test.py',
                "recheck": f'"{sys.executable}" recheck.py',
            }

            report = run_verification(request, workspace, workspace / "report.json")

            self.assertEqual(report["verification_status"], "REJECTED")
            self.assertEqual(report["remaining_selected_findings"], ["finding-md-001"])
            self.assertEqual(report["error"]["code"], "REPAIR_3001")

    def test_invalid_recheck_json_rejects_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            self.write_script(workspace, "build.py", "raise SystemExit(0)\n")
            self.write_script(workspace, "test.py", "raise SystemExit(0)\n")
            self.write_script(
                workspace,
                "recheck.py",
                "from pathlib import Path\nPath('evidence').mkdir(exist_ok=True)\nPath('evidence/recheck.json').write_text('{not-json', encoding='utf-8')\n",
            )
            request = self.make_request()
            request["commands"] = {
                "build": f'"{sys.executable}" build.py',
                "test": f'"{sys.executable}" test.py',
                "recheck": f'"{sys.executable}" recheck.py',
            }

            report = run_verification(request, workspace, workspace / "report.json")

            self.assertEqual(report["verification_status"], "REJECTED")
            self.assertEqual(report["error"]["stage"], "recheck")

    def test_invalid_recheck_shape_rejects_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            self.write_script(workspace, "build.py", "raise SystemExit(0)\n")
            self.write_script(workspace, "test.py", "raise SystemExit(0)\n")
            self.write_script(
                workspace,
                "recheck.py",
                "import json\nfrom pathlib import Path\nPath('evidence').mkdir(exist_ok=True)\nPath('evidence/recheck.json').write_text(json.dumps({'findings': [{'type': 'MISSING'}]}), encoding='utf-8')\n",
            )
            request = self.make_request()
            request["commands"] = {
                "build": f'"{sys.executable}" build.py',
                "test": f'"{sys.executable}" test.py',
                "recheck": f'"{sys.executable}" recheck.py',
            }

            report = run_verification(request, workspace, workspace / "report.json")

            self.assertEqual(report["verification_status"], "REJECTED")
            self.assertIn("finding_id", report["error"]["message"])

    def test_timeout_rejects_candidate_and_records_timeout(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            self.write_script(workspace, "build.py", "import time\ntime.sleep(2)\n")
            self.write_script(workspace, "test.py", "raise SystemExit(0)\n")
            self.write_script(workspace, "recheck.py", "raise SystemExit(0)\n")
            request = self.make_request()
            request["timeout_seconds"] = 0.1
            request["commands"] = {
                "build": f'"{sys.executable}" build.py',
                "test": f'"{sys.executable}" test.py',
                "recheck": f'"{sys.executable}" recheck.py',
            }

            report = run_verification(request, workspace, workspace / "report.json")

            self.assertEqual(report["verification_status"], "REJECTED")
            self.assertTrue(report["validation"]["build"]["timed_out"])
            self.assertTrue(report["validation"]["test"]["skipped"])

    def test_cli_returns_zero_for_accept_and_one_for_reject(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            self.write_script(workspace, "build.py", "raise SystemExit(0)\n")
            self.write_script(workspace, "test.py", "raise SystemExit(0)\n")
            self.write_script(
                workspace,
                "recheck.py",
                "import json\nfrom pathlib import Path\nPath('evidence').mkdir(exist_ok=True)\nPath('evidence/recheck.json').write_text(json.dumps({'findings': []}), encoding='utf-8')\n",
            )
            request = self.make_request()
            request["commands"] = {
                "build": f'"{sys.executable}" build.py',
                "test": f'"{sys.executable}" test.py',
                "recheck": f'"{sys.executable}" recheck.py',
            }
            request_path = workspace / "request.json"
            request_path.write_text(json.dumps(request), encoding="utf-8")
            accepted_output = workspace / "accepted.json"

            self.assertEqual(
                main(
                    [
                        "--request",
                        str(request_path),
                        "--workspace",
                        str(workspace),
                        "--output",
                        str(accepted_output),
                    ]
                ),
                0,
            )
            request["finding_ids"] = ["finding-md-001"]
            self.write_script(
                workspace,
                "recheck_remaining.py",
                "import json\nfrom pathlib import Path\nPath('evidence/recheck.json').write_text(json.dumps({'findings': [{'finding_id': 'finding-md-001'}]}), encoding='utf-8')\n",
            )
            request["commands"]["recheck"] = f'"{sys.executable}" recheck_remaining.py'
            request_path.write_text(json.dumps(request), encoding="utf-8")
            rejected_output = workspace / "rejected.json"

            self.assertEqual(
                main(
                    [
                        "--request",
                        str(request_path),
                        "--workspace",
                        str(workspace),
                        "--output",
                        str(rejected_output),
                    ]
                ),
                1,
            )

    def test_cli_returns_two_for_missing_workspace(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            request = self.make_request()
            request["commands"] = {
                "build": "build",
                "test": "test",
                "recheck": "recheck",
            }
            request_path = root / "request.json"
            output_path = root / "report.json"
            request_path.write_text(json.dumps(request), encoding="utf-8")

            result = main(
                [
                    "--request",
                    str(request_path),
                    "--workspace",
                    str(root / "missing-workspace"),
                    "--output",
                    str(output_path),
                ]
            )

            self.assertEqual(result, 2)
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
