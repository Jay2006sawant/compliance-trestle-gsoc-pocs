# POC-04 Crypto Compatibility Benchmark

| Algorithm | Signature size (bytes) | Sign time ms | Verify time ms | Valid verify | Wrong key | Corrupted signature | Invalid key/algorithm mismatch |
|---|---:|---:|---:|---|---|---|---|
| ECDSA_P256_SHA256 | 71 | 4.201 | 0.107 | PASS | FAIL_INVALID_SIGNATURE | FAIL_INVALID_SIGNATURE | FAIL_INVALID_SIGNATURE |
| RSA_PSS_SHA256 | 384 | 2.323 | 0.065 | PASS | FAIL_INVALID_SIGNATURE | FAIL_INVALID_SIGNATURE | FAIL_INVALID_SIGNATURE |
