# POC-05 Failure -> Message -> User Action

| Case | Failure | Message | User Action |
|---|---|---|---|
| C1 | missing OSCAL file | `[MISSING_OSCAL_FILE] OSCAL file not found: /home/jay/compliance-trestle/GSOC/POC/POC_5/artifacts/cases/missing-oscal.json` | Check the OSCAL path and ensure the file exists. |
| C2 | missing .sig file | `[MISSING_SIGNATURE_FILE] Signature file not found: /home/jay/compliance-trestle/GSOC/POC/POC_5/artifacts/cases/missing.sig` | Create the detached signature file or correct the .sig path. |
| C3 | digest mismatch | `[DIGEST_MISMATCH] Digest mismatch (expected db48a1381b8f6a38c1c26333c9c091a915dc4a5f4e2fff652ad5d63d2a411ae9, got b9f61ce614099c47d55546c18d6a5debbc9467a40ecfddfa1c59ea10ecbd4302).` | The artifact changed after signing; re-sign the exact payload. |
| C4 | invalid signature | `[INVALID_SIGNATURE] Signature verification failed for payload and key.` | Use the matching signer public key and regenerate signature if needed. |
| C5 | unsupported algorithm | `[UNSUPPORTED_ALGORITHM] Unsupported algorithm 'rsa-pss-sha512'.` | Use a supported algorithm (for MVP: ecdsa-p256-sha256). |
| C6 | malformed signature envelope | `[MALFORMED_SIGNATURE_ENVELOPE] Envelope is not valid JSON: Expecting property name enclosed in double quotes: line 1 column 3 (char 2)` | Fix envelope schema/fields and recreate the signature file. |
