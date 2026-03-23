#!/usr/bin/env python3
# Copyright (c) 2026 The OSCAL Compass Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Run every runnable GSOC PoC script and write a verification report.

Usage (from repo root):

  ./venv/bin/python POC/run_all_pocs.py

Exit code 0 only if every script exits 0.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

# (subdir, script_name) — order matches INDEX.md narrative
RUNNABLE_POCS: list[tuple[str, str]] = [
    ("POC_1", "run_poc01_demo.py"),
    ("POC_2", "run_poc02_canonicalization.py"),
    ("POC_3", "evaluate_envelope_options.py"),
    ("POC_4", "run_poc04_crypto_compat.py"),
    ("POC_5", "run_poc05_error_taxonomy.py"),
    ("POC_6", "generate_poc06_artifacts.py"),
    ("POC_7", "run_poc07_policy_modes.py"),
    ("POC_8", "generate_poc08_signing_decision.py"),
    ("POC_9", "run_poc09_provenance_demo.py"),
    ("POC_10", "generate_poc10_threat_model.py"),
    ("POC_11", "generate_poc11_test_strategy.py"),
    ("POC_12", "generate_poc12_docs_usability.py"),
]

REPORT_PATH = ROOT / "artifacts" / "poc_verification_report.txt"


def python_exe() -> Path:
    v = REPO_ROOT / "venv" / "bin" / "python"
    if v.is_file():
        return v
    return Path(sys.executable)


def main() -> int:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    py = python_exe()
    lines: list[str] = [
        "GSOC PoC verification run",
        f"Time (UTC): {datetime.now(timezone.utc).isoformat()}",
        f"Python: {py}",
        f"Repo: {REPO_ROOT}",
        "",
    ]
    failed: list[str] = []
    for subdir, script in RUNNABLE_POCS:
        path = ROOT / subdir / script
        if not path.is_file():
            failed.append(f"{subdir}/{script} (missing file)")
            lines.append(f"FAIL  missing: {path}")
            continue
        r = subprocess.run(
            [str(py), str(path)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        if r.returncode == 0:
            lines.append(f"OK    {subdir}/{script}")
        else:
            failed.append(f"{subdir}/{script}")
            lines.append(f"FAIL  {subdir}/{script} (exit {r.returncode})")
            if r.stderr:
                lines.append("  stderr: " + r.stderr[:2000])
            if r.stdout:
                lines.append("  stdout: " + r.stdout[:2000])

    lines.append("")
    lines.append(f"Total: {len(RUNNABLE_POCS)} scripts, {len(failed)} failed.")
    text = "\n".join(lines) + "\n"
    REPORT_PATH.write_text(text, encoding="utf-8")
    print(text)
    if failed:
        print(f"Verification FAILED ({len(failed)} script(s)). See {REPORT_PATH}", file=sys.stderr)
        return 1
    print(f"Verification OK. Report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
