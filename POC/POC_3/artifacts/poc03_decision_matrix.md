# POC-03 Signature Envelope Decision Matrix

## Criteria and weights

| Criterion | Weight | Why it matters |
|---|---:|---|
| Compatibility with current trestle code | 4 | Lower change risk helps deliver a working MVP quickly. |
| Migration complexity | 3 | We need an approach that can evolve without rewriting everything. |
| Interoperability | 4 | Cross-tool verification and ecosystem alignment are long-term goals. |
| Metadata and provenance support | 3 | Auditability and traceability matter for compliance workflows. |

## Option scoring

| Option | Compatibility (x4) | Migration (x3) | Interop (x4) | Metadata (x3) | Weighted total |
|---|---:|---:|---:|---:|---:|
| Custom minimal detached envelope | 5 | 5 | 2 | 3 | 52 |
| DSSE-style envelope | 3 | 2 | 5 | 4 | 50 |
| JWS-style envelope | 2 | 2 | 4 | 4 | 42 |

## Recommendation

Selected baseline for MVP: **Custom minimal detached envelope**

Rationale:
- Delivers working value quickly with low integration risk.
- Preserves a clear migration path to DSSE as interoperability needs increase.

## Migration path to DSSE/Sigstore

1. Keep detached signature verification stable for MVP users.
2. Expand metadata fields to capture provenance context.
3. Introduce DSSE-compatible envelope adapter and validation mode.
4. Add Sigstore-oriented flow in a future phase (keyless/certificate-based trust model).
