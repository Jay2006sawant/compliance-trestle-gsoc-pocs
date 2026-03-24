# POC-07: Policy mode behavior simulation (`off|warn|enforce`)

This PoC demonstrates rollout behavior for signature policy modes.

## Current status

- Verified successfully from the repository root with `python3 POC/run_all_pocs.py`
- Primary evidence: `artifacts/poc07_policy_behavior.md` and `artifacts/poc07_policy_behavior.json`

## Objective

Show predictable handling for:
- signed valid file
- unsigned file
- signed tampered file

Across policy modes:
- `off`
- `warn`
- `enforce`

## Run

From repository root:

```bash
./venv/bin/python POC/POC_7/run_poc07_policy_modes.py
```

## Evidence artifacts

Generated in `POC/POC_7/artifacts/`:
- `poc07_policy_behavior.json`
- `poc07_policy_behavior.md`
- `poc07_transcript.txt`
