# POC-02: Canonicalization determinism proof

This PoC demonstrates deterministic digest generation for logically identical JSON representations.

## Objective

Show:
- same semantic object -> same digest
- changed semantic value -> different digest

## Method

The script builds multiple textual JSON variants of the same object:
- different key order
- pretty vs compact output
- different whitespace

Then it:
- parses each JSON payload
- applies a deterministic canonicalization profile
- computes SHA-256 digests and compares them

## Canonicalization profile used

Profile in this PoC:
- `json.loads()` parse
- `json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)`
- SHA-256 over UTF-8 bytes

Note:
- This is a practical deterministic profile for validation.
- It is not a full implementation of RFC 8785 canonical JSON.
- We can upgrade to stricter RFC 8785 behavior later if needed.

## Run

From repository root:

```bash
./venv/bin/python POC/POC_2/run_poc02_canonicalization.py
```

Run with a real OSCAL JSON:

```bash
./venv/bin/python POC/POC_2/run_poc02_canonicalization.py \
  --input-json nist-content/examples/catalog/json/basic-catalog.json
```

## Evidence artifacts

Generated in `POC/POC_2/artifacts/`:
- `poc02_digest_results.json`
- `poc02_digest_table.md`
- `poc02_transcript.txt`
