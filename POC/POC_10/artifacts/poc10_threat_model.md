# POC-10 Threat Model Table

| Threat | Impact | Mitigation | Non-goal |
|---|---|---|---|
| Tampering after signing | Compromised artifact integrity and trust | Digest+signature verification on read/validate; enforce mode in sensitive workflows | Preventing all unauthorized file modifications on disk |
| Fake signer key substitution | Attacker can appear as trusted signer | Trusted key registry/fingerprint pinning and key rotation policy | Global PKI trust bootstrapping in MVP |
| Key leakage | Unauthorized signatures accepted as legitimate | Key storage hygiene, rotation, revocation list, HSM/KMS in future phase | Full enterprise key management rollout in MVP |
| Replay of old artifact | Outdated vulnerable content accepted | Version/timestamp checks, policy for freshness windows, provenance metadata review | Perfect prevention of every offline replay scenario |
| Malformed envelope parsing abuse | Parser confusion or denial-of-service pathways | Strict schema validation, bounded parsing, explicit error taxonomy | Mitigating unrelated parser bugs outside signature envelope scope |
