# OSCAL Signing Quick Start (POC-12)

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
