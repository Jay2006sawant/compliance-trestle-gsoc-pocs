# OSCAL Signing PoC Lab

This folder contains all proofs of concept for the OSCAL signing and verification
project.

## Current status

- All PoC runners execute successfully from the repository root.
- Smoke tests pass for the key paths covered by `POC/test_poc_smoke.py`.
- Generated evidence is stored alongside each PoC under its `artifacts/`
  directory.

## Goals

- Show working evidence, not only ideas
- Reduce project risk before implementation phases
- Attach demos and analysis alongside the PoC track

## Execution model

- One PoC folder per topic (`poc-01` to `poc-12`)
- Each PoC has a `README.md` with objective, method, run steps, output, and result
- The PoCs are designed to be reproducible from the repository root

## Layout

- `INDEX.md` — tracker of all PoCs
- `run_all_pocs.py` — runs every PoC script; writes `artifacts/poc_verification_report.txt`
- `test_poc_smoke.py` — stdlib unittest smoke checks (no pytest required)
- `POC_1` … `POC_12` — individual PoCs
- `artifacts/poc_verification_report.txt` — aggregate verification report for the latest repo-root run

## Verify everything (repo root)

```bash
python3 POC/run_all_pocs.py
python3 -m unittest POC/test_poc_smoke.py -v
```
