import json
from hashlib import sha256
from typing import Any

def canonicalize_json(value: Any) -> bytes:
    # Convert JSON object into a deterministic string:
    # - keys sorted
    # - no extra spaces
    # - stable UTF-8 output
    normalized = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return normalized.encode("utf-8")

def canonical_digest(value: Any) -> str:
    # Hash canonical bytes so same semantic JSON gives same digest
    return sha256(canonicalize_json(value)).hexdigest()


import base64
from hashlib import sha256
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

def sign_payload(payload_bytes: bytes, private_key) -> dict:
    # Compute payload digest for integrity tracking
    digest = sha256(payload_bytes).hexdigest()

    # Create ECDSA signature over payload bytes
    sig = private_key.sign(payload_bytes, ec.ECDSA(hashes.SHA256()))

    # Build detached signature envelope (.sig content)
    return {
        "algorithm": "ecdsa-p256-sha256",
        "payload_sha256": digest,
        "signature_b64": base64.b64encode(sig).decode("ascii"),
    }



import base64
from hashlib import sha256
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

def verify_payload(payload_bytes: bytes, envelope: dict, public_key) -> str:
    # 1) Reject unsupported algorithms early
    if envelope.get("algorithm") != "ecdsa-p256-sha256":
        return "UNSUPPORTED_ALGORITHM"

    # 2) Verify integrity first (detect post-sign tampering)
    actual = sha256(payload_bytes).hexdigest()
    if actual != envelope["payload_sha256"]:
        return "DIGEST_MISMATCH"

    # 3) Verify cryptographic signature using signer public key
    sig = base64.b64decode(envelope["signature_b64"])
    public_key.verify(sig, payload_bytes, ec.ECDSA(hashes.SHA256()))

    # If all checks pass, artifact is trusted
    return "VERIFIED"



class VerificationError(Exception):
    # Base class for all verification failures
    code = "UNKNOWN_ERROR"
    remediation = "Review inputs and retry."

class DigestMismatchError(VerificationError):
    # Payload changed after signing
    code = "DIGEST_MISMATCH"
    remediation = "The artifact changed after signing; re-sign the exact payload."

class UnsupportedAlgorithmError(VerificationError):
    # Signature uses algorithm not enabled in MVP
    code = "UNSUPPORTED_ALGORITHM"
    remediation = "Use a supported algorithm (for MVP: ecdsa-p256-sha256)."


```python
def apply_signature_policy(policy: str, verify_status: str) -> tuple[bool, str]:
    # verify_status can be: VERIFIED, UNSIGNED, DIGEST_MISMATCH, INVALID_SIGNATURE, MALFORMED_ENVELOPE
    if policy == "off":
        # preserve existing behavior for backward compatibility
        return True, "Signature checks are disabled."


    if verify_status == "VERIFIED":
        # trusted artifact, always continue
        return True, "Signature verified."


    if policy == "warn":
        # continue but make issue explicit
        return True, f"Warning: {verify_status}"


    # policy == "enforce"
    return False, f"Blocked due to signature policy: {verify_status}"





def apply_signature_policy(policy: str, verify_status: str) -> tuple[bool, str]:
    # verify_status can be: VERIFIED, UNSIGNED, DIGEST_MISMATCH, INVALID_SIGNATURE, MALFORMED_ENVELOPE
    if policy == "off":
        # preserve existing behavior for backward compatibility
        return True, "Signature checks are disabled."

    if verify_status == "VERIFIED":
        # trusted artifact, always continue
        return True, "Signature verified."

    if policy == "warn":
        # continue but make issue explicit
        return True, f"Warning: {verify_status}"

    # policy == "enforce"
    return False, f"Blocked due to signature policy: {verify_status}"

def maybe_sign_after_write(oscal_path, signing_enabled, private_key):
    if not signing_enabled:
        return None

    payload = oscal_path.read_bytes()
    envelope = build_signature_envelope(payload, private_key)  # from M1 core logic
    sig_path = oscal_path.with_suffix(oscal_path.suffix + ".sig")
    sig_path.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
    return sig_path

ERROR_HELP = {
    "UNSIGNED": "No signature file found. Sign artifact or use policy=warn/off during migration.",
    "DIGEST_MISMATCH": "Artifact changed after signing. Re-sign the exact payload.",
    "INVALID_SIGNATURE": "Signature does not match payload/key. Use the correct public key.",
    "MALFORMED_ENVELOPE": "Signature file format is invalid. Recreate the signature.",
}


from datetime import datetime, timezone

def add_provenance(envelope: dict, signer_id: str, tool_version: str, commit_id: str | None) -> dict:
    # Copy to avoid mutating original structure in-place
    out = dict(envelope)

    # Add metadata useful for audits and incident debugging
    out["provenance"] = {
        "signer": signer_id,
        "tool": "trestle",
        "tool_version": tool_version,
        "signed_at": datetime.now(timezone.utc).isoformat(),
        "commit_id": commit_id,
    }
    return out


```python
import base64


ALLOWED_ALGOS = {"ecdsa-p256-sha256"}


def validate_envelope(envelope: dict) -> None:
    required = {"algorithm", "payload_sha256", "signature_b64"}
    missing = sorted(required - set(envelope.keys()))
    if missing:
        raise ValueError(f"Missing envelope fields: {', '.join(missing)}")


    if envelope["algorithm"] not in ALLOWED_ALGOS:
        raise ValueError(f"Unsupported algorithm: {envelope['algorithm']}")


    # strict base64 decode to reject malformed signatures early
    base64.b64decode(envelope["signature_b64"], validate=True)
```


def test_backward_compat_without_provenance():
    # Old envelope without provenance should still verify
    envelope = {
        "algorithm": "ecdsa-p256-sha256",
        "payload_sha256": "...",
        "signature_b64": "...",
    }
    assert verify_detached(sample_payload_bytes, envelope, sample_public_key) == "VERIFIED"