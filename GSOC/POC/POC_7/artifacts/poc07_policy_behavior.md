# POC-07 Policy Mode Behavior Matrix

| Mode | File condition | Behavior | Reason |
|---|---|---|---|
| off | signed_valid | ALLOW | Signature checks disabled by policy. |
| off | unsigned | ALLOW | Signature checks disabled by policy. |
| off | signed_tampered | ALLOW | Signature checks disabled by policy. |
| warn | signed_valid | ALLOW | Valid signature. |
| warn | unsigned | ALLOW_WITH_WARNING | UNSIGNED: No detached signature found. |
| warn | signed_tampered | ALLOW_WITH_WARNING | DIGEST_MISMATCH: Payload digest differs from signature envelope. |
| enforce | signed_valid | ALLOW | Valid signature. |
| enforce | unsigned | BLOCK | UNSIGNED: No detached signature found. |
| enforce | signed_tampered | BLOCK | DIGEST_MISMATCH: Payload digest differs from signature envelope. |
