# POC-03: Signature envelope design comparison

This PoC compares envelope approaches for detached OSCAL signatures and records an evidence-backed MVP decision.

## Current status

- Verified successfully from the repository root with `python3 POC/run_all_pocs.py`
- Primary evidence: `artifacts/poc03_decision_matrix.md` and `artifacts/poc03_decision_matrix.json`

## Objective

Choose an initial envelope strategy for trestle MVP, then define a migration path to DSSE/Sigstore-friendly approaches.

Compared options:
- custom minimal detached envelope
- DSSE-style envelope
- JWS-style envelope

Criteria:
- compatibility with current trestle code
- migration complexity
- interoperability
- metadata/provenance support

## Method

The script applies weighted scoring across criteria and emits:
- machine-readable matrix (`.json`)
- proposal-ready decision table (`.md`)
- transcript summary

## Run

From repository root:

```bash
./venv/bin/python POC/POC_3/evaluate_envelope_options.py
```

## Evidence artifacts

Generated in `POC/POC_3/artifacts/`:
- `poc03_decision_matrix.json`
- `poc03_decision_matrix.md`
- `poc03_transcript.txt`

## Expected outcome

- Clear rationale for starting MVP with minimal detached envelope
- Explicit migration path toward DSSE/Sigstore-compatible future phases
