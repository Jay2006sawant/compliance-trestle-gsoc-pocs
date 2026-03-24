# POC-08: Import/assemble pipeline signing decision

This PoC compares where signing should occur in the artifact lifecycle.

## Current status

- Verified successfully from the repository root with `python3 POC/run_all_pocs.py`
- Primary evidence: `artifacts/poc08_sequence_and_recommendation.md` and `artifacts/poc08_decision.json`

## Objective

Evaluate:
- manual signing only
- automatic signing post-validation
- signing at assemble/publish stage

Then provide recommendation with tradeoffs.

## Run

```bash
./venv/bin/python POC/POC_8/generate_poc08_signing_decision.py
```

## Artifacts

Generated in `POC/POC_8/artifacts/`:
- `poc08_decision.json`
- `poc08_sequence_and_recommendation.md`
- `poc08_transcript.txt`
