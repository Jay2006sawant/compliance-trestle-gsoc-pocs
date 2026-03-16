# POC-02 Digest Comparison Table

| Case | Semantic Group | Raw SHA-256 | Canonical SHA-256 |
|---|---|---|---|
| A_pretty | A | `276ebedf7f6db8afcae84b31a1996d400ec259462c37814d60f8a243dd8bf399` | `251224835c4556a4dececa7289959bc4c66d9718af1f63f260e8ebd4f5ad18ee` |
| A_compact | A | `1cb5d3acfdcb3c1dd258695fa61aa5f47d7e481188c8a282d7a88ab9dfc6e651` | `251224835c4556a4dececa7289959bc4c66d9718af1f63f260e8ebd4f5ad18ee` |
| A_sorted | A | `703f6bfa16c112e5c718803cd7081faadcb8d2774bd5712bcfe9523d70af37e3` | `251224835c4556a4dececa7289959bc4c66d9718af1f63f260e8ebd4f5ad18ee` |
| B_changed_semantic_value | B | `5f65d50977388ccc9406cd454a41f5e3246be81931bf88a8f64cd3471826353b` | `5827a4635eaea3516e9b9b9acaf097f47e1189a4852f83667def7aa116e003bc` |

## Interpretation

- Group A cases represent the same semantic object with different formatting/key order.
- Canonical digests for Group A must match.
- Group B changes a semantic value and must produce a different canonical digest.
