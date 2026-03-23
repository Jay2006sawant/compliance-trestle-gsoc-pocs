# POC-05: Error taxonomy and UX PoC

This PoC verifies that signature verification failures are precise and actionable.

## Objective

Trigger each expected failure and capture:
- failure type
- exact error message
- remediation hint for user action

Covered failures:
- missing OSCAL file
- missing `.sig` file
- digest mismatch
- invalid signature
- unsupported algorithm
- malformed signature envelope

## Run

From repository root:

```bash
./venv/bin/python POC/POC_5/run_poc05_error_taxonomy.py
```

## Evidence artifacts

Generated in `POC/POC_5/artifacts/`:
- `poc05_error_results.json`
- `poc05_error_matrix.md`
- `poc05_transcript.txt`

## Success criteria

Each failure should provide a precise remediation hint so users can recover quickly.
