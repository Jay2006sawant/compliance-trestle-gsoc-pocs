# POC-07: Policy mode behavior simulation (`off|warn|enforce`)

This PoC demonstrates rollout behavior for signature policy modes.

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
./venv/bin/python GSOC/POC/POC_7/run_poc07_policy_modes.py
```

## Evidence artifacts

Generated in `GSOC/POC/POC_7/artifacts/`:
- `poc07_policy_behavior.json`
- `poc07_policy_behavior.md`
- `poc07_transcript.txt`
