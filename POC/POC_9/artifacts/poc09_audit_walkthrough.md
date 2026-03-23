# POC-09 Provenance Walkthrough

## Scenario

Two artifacts are both cryptographically signed, but an auditor needs traceability:
- who signed each artifact
- when it was signed
- which tool/build produced it
- which source revision produced it

## How metadata helps

- `signer_identity` distinguishes signer ownership and accountability.
- `timestamp_utc` supports timeline reconstruction during incident review.
- `tool_name` + `tool_version` clarify verifier compatibility and reproducibility.
- `build_id` links artifact to CI/CD execution evidence.
- `git_commit` connects artifact to exact source state.

## Auditor mini-check

1. Compare `artifact_a.envelope.json` and `artifact_b.envelope.json`.
2. Observe different signer/build metadata.
3. Use `git_commit` + `build_id` to retrieve corresponding pipeline logs.
4. Confirm whether provenance aligns with release policy.
