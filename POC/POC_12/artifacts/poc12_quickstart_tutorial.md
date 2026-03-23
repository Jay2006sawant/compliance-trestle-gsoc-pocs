# OSCAL Signing Quick Start (POC-12)

## Prerequisites
- project checked out locally
- virtual environment available at `./venv`

## 1) Create sample OSCAL model

```bash
mkdir -p POC/POC_1/workspace
./venv/bin/python -m trestle init -loc -tr POC/POC_1/workspace
./venv/bin/python -m trestle create -t catalog -o sample-catalog -x json -tr POC/POC_1/workspace
```

## 2) Run detached signing demo

```bash
./venv/bin/python POC/POC_1/run_poc01_demo.py
```

## 3) Verify expected outcomes

- Step 1: valid file -> PASS
- Step 2: tampered file with old signature -> FAIL (digest mismatch)
- Step 3: re-signed tampered file -> PASS

## 4) Inspect generated evidence

Check:
- `POC/POC_1/artifacts/poc01_transcript.txt`
- `POC/POC_1/artifacts/*.sig`
- `POC/POC_1/artifacts/*.json`
