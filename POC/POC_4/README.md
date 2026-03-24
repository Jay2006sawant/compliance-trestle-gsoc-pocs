# POC-04: Crypto algorithm compatibility benchmark

This PoC validates detached signature behavior with both ECDSA P-256 and RSA-PSS.

## Current status

- Verified successfully from the repository root with `python3 POC/run_all_pocs.py`
- Primary evidence: `artifacts/poc04_benchmark_table.md` and `artifacts/poc04_benchmark_results.json`

## Objective

- Verify both algorithms sign and verify the same payload reliably
- Demonstrate clear failures for wrong key, corrupted signature, and algorithm/key mismatch
- Capture rough size/time comparison for proposal evidence

## Run

From repository root:

```bash
./venv/bin/python POC/POC_4/run_poc04_crypto_compat.py
```

Run with a real OSCAL JSON:

```bash
./venv/bin/python POC/POC_4/run_poc04_crypto_compat.py \
  --input-json nist-content/examples/catalog/json/basic-catalog.json
```

## Evidence artifacts

Generated in `POC/POC_4/artifacts/`:
- `poc04_payload_digest.txt`
- `poc04_benchmark_results.json`
- `poc04_benchmark_table.md`
- `poc04_transcript.txt`
