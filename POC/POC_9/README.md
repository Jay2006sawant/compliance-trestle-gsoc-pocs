# POC-09: Provenance metadata usefulness demo

This PoC shows how signature metadata improves auditing and troubleshooting.

## Objective

Demonstrate usefulness of metadata fields:
- tool name/version
- model type
- signer identity
- timestamp
- git commit
- build id

## Run

```bash
./venv/bin/python POC/POC_9/run_poc09_provenance_demo.py
```

## Artifacts

Generated in `POC/POC_9/artifacts/`:
- `artifact_a.envelope.json`
- `artifact_b.envelope.json`
- `poc09_audit_walkthrough.md`
- `poc09_transcript.txt`
