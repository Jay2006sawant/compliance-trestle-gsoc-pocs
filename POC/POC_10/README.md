# POC-10: Security threat-model mini analysis

This PoC captures realistic signature-related threats and mitigations.

## Objective

Cover:
- tampering after signing
- fake signer key
- key leakage risk
- replay/old artifact acceptance
- malformed envelope parsing abuse

## Run

```bash
./venv/bin/python POC/POC_10/generate_poc10_threat_model.py
```

## Artifacts

Generated in `POC/POC_10/artifacts/`:
- `poc10_threat_model.json`
- `poc10_threat_model.md`
- `poc10_transcript.txt`
