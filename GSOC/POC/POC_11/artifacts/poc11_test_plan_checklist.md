# POC-11 Test Strategy Checklist

## Unit tests
- [ ] canonicalization deterministic output
- [ ] envelope schema validation
- [ ] digest mismatch detection
- [ ] ECDSA sign/verify path
- [ ] RSA-PSS sign/verify path

## Integration tests
- [ ] `sign` command creates detached signature file
- [ ] `verify` command passes valid file
- [ ] `verify` command fails tampered file with actionable message

## Negative/failure tests
- [ ] missing OSCAL file
- [ ] missing signature file
- [ ] malformed envelope
- [ ] unsupported algorithm
- [ ] wrong key / invalid signature

## Regression tests
- [ ] existing trestle write flows still work when signing is disabled
- [ ] existing validate workflows remain backward compatible in warn mode
- [ ] performance remains acceptable for baseline models
