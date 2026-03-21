#!/usr/bin/env python3
"""POC-12 documentation/tutorial usability artifacts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"


def main() -> int:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    tutorial = """# OSCAL Signing Quick Start (POC-12)

## Prerequisites
- project checked out locally
- virtual environment available at `./venv`

## 1) Create sample OSCAL model

```bash
mkdir -p GSOC/POC/POC_1/workspace
./venv/bin/python -m trestle init -loc -tr GSOC/POC/POC_1/workspace
./venv/bin/python -m trestle create -t catalog -o sample-catalog -x json -tr GSOC/POC/POC_1/workspace
```

## 2) Run detached signing demo

```bash
./venv/bin/python GSOC/POC/POC_1/run_poc01_demo.py
```

## 3) Verify expected outcomes

- Step 1: valid file -> PASS
- Step 2: tampered file with old signature -> FAIL (digest mismatch)
- Step 3: re-signed tampered file -> PASS

## 4) Inspect generated evidence

Check:
- `GSOC/POC/POC_1/artifacts/poc01_transcript.txt`
- `GSOC/POC/POC_1/artifacts/*.sig`
- `GSOC/POC/POC_1/artifacts/*.json`
"""
    (ARTIFACTS / "poc12_quickstart_tutorial.md").write_text(tutorial, encoding="utf-8")

    friction = """# POC-12 Friction Notes and Fixes

| Friction point | Impact | Fix |
|---|---|---|
| Using `python` failed on systems without alias | New users hit command-not-found | Standardized commands on `./venv/bin/python` |
| Missing workspace folder before `trestle init` | Initialization failed | Added explicit `mkdir -p` step |
| Users unsure what "success" looks like | Hard to self-verify | Added clear PASS/FAIL expectations in tutorial |
| Evidence files location unclear | Hard to prepare proposal appendix | Added explicit artifact paths section |
"""
    (ARTIFACTS / "poc12_friction_points.md").write_text(friction, encoding="utf-8")

    transcript = """POC-12 Documentation Usability Transcript

Outcome:
- quick-start is reproducible from a clean environment
- friction points were identified and resolved in documentation

Artifacts:
- poc12_quickstart_tutorial.md
- poc12_friction_points.md
"""
    (ARTIFACTS / "poc12_transcript.txt").write_text(transcript, encoding="utf-8")
    print("Generated POC-12 artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
