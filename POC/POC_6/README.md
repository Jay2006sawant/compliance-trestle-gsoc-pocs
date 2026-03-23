# POC-06: Trestle workflow integration check

This PoC maps where OSCAL signing and verification should hook into trestle write/read flows.

## Objective

Demonstrate that signing design fits current trestle architecture and identify any bypass paths.

## Method

- trace write path (`WriteFileAction` and related command flows)
- trace direct write path (`oscal_write` usage in tasks/author commands)
- trace read/validate path (`oscal_read`, `Validator`, distributed loading)
- identify hook points and any unsigned-path gaps

## Run

From repository root:

```bash
./venv/bin/python POC/POC_6/generate_poc06_artifacts.py
```

## Evidence artifacts

Generated in `POC/POC_6/artifacts/`:
- `poc06_hook_points.json`
- `poc06_architecture_hook_map.md`
- `poc06_transcript.txt`

## Expected outcome

- Architecture map and file/function hook map are explicit
- MVP hook points are clearly identified
- Bypass/gap paths are documented with mitigation
