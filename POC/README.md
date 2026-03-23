# OSCAL Signing PoC Lab

This folder contains all GSoC Proofs of Concept (PoCs) for the OSCAL signing and verification project.

## Goals

- Show working evidence, not only ideas
- Reduce project risk before implementation phases
- Attach demos and analysis alongside the PoC track

## Execution model

- One PoC folder per topic (`poc-01` to `poc-12`)
- Each PoC has a `README.md` with objective, method, run steps, output, and result
- We complete and verify PoCs in sequence

## Layout

- `INDEX.md` — tracker of all PoCs
- `run_all_pocs.py` — runs every PoC script; writes `artifacts/poc_verification_report.txt`
- `test_poc_smoke.py` — stdlib unittest smoke checks (no pytest required)
- `POC_1` … `POC_12` — individual PoCs

## Verify everything (repo root)

```bash
./venv/bin/python POC/run_all_pocs.py
./venv/bin/python -m unittest POC/test_poc_smoke.py -v
```
