# POC-04 Crypto Compatibility Benchmark

| Algorithm | Signature size (bytes) | Sign time ms | Verify time ms | Valid verify | Wrong key | Corrupted signature | Invalid key/algorithm mismatch |
|---|---:|---:|---:|---|---|---|---|
| ECDSA_P256_SHA256 | 71 | 4.361 | 0.111 | PASS | FAIL_INVALID_SIGNATURE | FAIL_INVALID_SIGNATURE | FAIL_INVALID_SIGNATURE |
| RSA_PSS_SHA256 | 384 | 2.069 | 0.046 | PASS | FAIL_INVALID_SIGNATURE | FAIL_INVALID_SIGNATURE | FAIL_INVALID_SIGNATURE |
