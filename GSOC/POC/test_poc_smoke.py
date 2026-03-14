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
"""Smoke tests for GSOC PoC scripts (stdlib only — no pytest required).

Run from repo root:

  ./venv/bin/python -m unittest GSOC/POC/test_poc_smoke.py -v

Optional (if pytest is installed):

  pytest GSOC/POC/test_poc_smoke.py -v
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent


def _canon(obj: object) -> bytes:
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _python() -> Path:
    v = REPO / "venv" / "bin" / "python"
    if v.is_file():
        return v
    return Path(sys.executable)


class TestCanonicalJson(unittest.TestCase):
    def test_same_semantics_same_digest(self) -> None:
        a = {"metadata": {"title": "x"}, "uuid": "z"}
        b = {"uuid": "z", "metadata": {"title": "x"}}
        self.assertEqual(sha256(_canon(a)).hexdigest(), sha256(_canon(b)).hexdigest())

    def test_change_changes_digest(self) -> None:
        x = {"a": 1}
        y = {"a": 2}
        self.assertNotEqual(sha256(_canon(x)).hexdigest(), sha256(_canon(y)).hexdigest())


class TestPoCScripts(unittest.TestCase):
    def test_run_all_pocs_exits_zero(self) -> None:
        runner = ROOT / "run_all_pocs.py"
        r = subprocess.run(
            [str(_python()), str(runner)],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            timeout=300,
        )
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)

    def test_poc01_poc02_poc05(self) -> None:
        for subdir, script in [
            ("POC_1", "run_poc01_demo.py"),
            ("POC_2", "run_poc02_canonicalization.py"),
            ("POC_5", "run_poc05_error_taxonomy.py"),
        ]:
            path = ROOT / subdir / script
            r = subprocess.run(
                [str(_python()), str(path)],
                cwd=str(REPO),
                capture_output=True,
                text=True,
                timeout=120,
            )
            self.assertEqual(r.returncode, 0, msg=f"{path}: {r.stderr}")


if __name__ == "__main__":
    unittest.main()
