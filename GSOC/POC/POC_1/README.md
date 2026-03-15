# POC-01: End-to-end detached signing MVP demo

This PoC demonstrates detached signing and verification for OSCAL JSON (see `INDEX.md` POC-01).

## Objective

Prove we can:
- Sign OSCAL JSON using a private key and detached `.sig` file
- Verify valid file successfully
- Detect tampering with clear digest mismatch
- Re-sign and verify pass again

## What is included

- `run_poc01_demo.py`: end-to-end PoC runner
- `workspace/`: local trestle workspace used to generate sample OSCAL content
- `keys/`: generated ECDSA keypair for the demo
- `artifacts/`: generated JSON, `.sig`, and transcript evidence

## Run steps

From repository root:

1) Generate sample OSCAL JSON with trestle:

```bash
mkdir -p GSOC/POC/POC_1/workspace
./venv/bin/python -m trestle init -loc -tr GSOC/POC/POC_1/workspace
./venv/bin/python -m trestle create -t catalog -o sample-catalog -x json -tr GSOC/POC/POC_1/workspace
```

2) Run the detached signing PoC:

```bash
./venv/bin/python GSOC/POC/POC_1/run_poc01_demo.py
```

## Run with real OSCAL example

Use an existing OSCAL JSON from `nist-content/examples`:

```bash
./venv/bin/python GSOC/POC/POC_1/run_poc01_demo.py \
  --input-json nist-content/examples/catalog/json/basic-catalog.json
```

## Evidence artifacts (generated)

Inside `GSOC/POC/POC_1/artifacts/`:
- `sample-catalog.original.json`
- `sample-catalog.original.sig`
- `sample-catalog.tampered.json`
- `sample-catalog.tampered.sig`
- `poc01_transcript.txt`

## Success criteria mapping

- Valid file verification passes (Step 1)
- Tampered file verification fails with digest mismatch (Step 2)
- Re-signed tampered file verification passes (Step 3)
