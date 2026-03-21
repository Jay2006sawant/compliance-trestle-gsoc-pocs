"""Sample test skeleton for signing PoC."""


def test_canonicalization_same_semantics_same_digest() -> None:
    # TODO: arrange same semantic JSON with different formatting
    # TODO: assert canonical digests match
    assert True


def test_verify_tampered_payload_fails_with_digest_mismatch() -> None:
    # TODO: create signed payload then modify one field
    # TODO: assert verify result includes DIGEST_MISMATCH
    assert True


def test_policy_enforce_blocks_unsigned() -> None:
    # TODO: run verify in enforce mode without signature
    # TODO: assert block behavior and remediation hint
    assert True
