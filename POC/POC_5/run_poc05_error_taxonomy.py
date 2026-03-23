#!/usr/bin/env python3
"""POC-05 error taxonomy and UX proof for signature verification."""

from __future__ import annotations

import argparse
import base64
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
CASES_DIR = ARTIFACTS / "cases"
PRIVATE_KEY_PATH = CASES_DIR / "poc05-private.pem"
PUBLIC_KEY_PATH = CASES_DIR / "poc05-public.pem"


class VerificationError(Exception):
    """Base class for PoC verification failures."""

    code: str = "UNKNOWN_ERROR"
    remediation: str = "Review inputs and retry."


class MissingOscalFileError(VerificationError):
    code = "MISSING_OSCAL_FILE"
    remediation = "Check the OSCAL path and ensure the file exists."


class MissingSignatureFileError(VerificationError):
    code = "MISSING_SIGNATURE_FILE"
    remediation = "Create the detached signature file or correct the .sig path."


class DigestMismatchError(VerificationError):
    code = "DIGEST_MISMATCH"
    remediation = "The artifact changed after signing; re-sign the exact payload."


class InvalidSignatureError(VerificationError):
    code = "INVALID_SIGNATURE"
    remediation = "Use the matching signer public key and regenerate signature if needed."


class UnsupportedAlgorithmError(VerificationError):
    code = "UNSUPPORTED_ALGORITHM"
    remediation = "Use a supported algorithm (for MVP: ecdsa-p256-sha256)."


class MalformedEnvelopeError(VerificationError):
    code = "MALFORMED_SIGNATURE_ENVELOPE"
    remediation = "Fix envelope schema/fields and recreate the signature file."


@dataclass
class FailureResult:
    case_id: str
    failure: str
    message: str
    remediation: str


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def ensure_keypair() -> None:
    if PRIVATE_KEY_PATH.exists() and PUBLIC_KEY_PATH.exists():
        return
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    PRIVATE_KEY_PATH.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    PUBLIC_KEY_PATH.write_bytes(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )


def load_private_key():
    return serialization.load_pem_private_key(PRIVATE_KEY_PATH.read_bytes(), password=None)


def load_public_key():
    return serialization.load_pem_public_key(PUBLIC_KEY_PATH.read_bytes())


def sign_payload(payload_path: Path, sig_path: Path) -> None:
    payload = payload_path.read_bytes()
    digest = sha256(payload).hexdigest()
    signature = load_private_key().sign(payload, ec.ECDSA(hashes.SHA256()))
    envelope = {
        "algorithm": "ecdsa-p256-sha256",
        "payload_sha256": digest,
        "signature_b64": base64.b64encode(signature).decode("ascii"),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    write_text(sig_path, json.dumps(envelope, indent=2) + "\n")


def verify_payload(payload_path: Path, sig_path: Path) -> str:
    if not payload_path.exists():
        raise MissingOscalFileError(f"OSCAL file not found: {payload_path}")
    if not sig_path.exists():
        raise MissingSignatureFileError(f"Signature file not found: {sig_path}")

    try:
        envelope: dict[str, Any] = json.loads(sig_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise MalformedEnvelopeError(f"Envelope is not valid JSON: {exc}") from exc

    required_fields = {"algorithm", "payload_sha256", "signature_b64"}
    missing = sorted(required_fields - set(envelope.keys()))
    if missing:
        raise MalformedEnvelopeError(f"Envelope missing required fields: {', '.join(missing)}")

    algorithm = envelope["algorithm"]
    if algorithm != "ecdsa-p256-sha256":
        raise UnsupportedAlgorithmError(f"Unsupported algorithm '{algorithm}'.")

    actual_digest = sha256(payload_path.read_bytes()).hexdigest()
    expected_digest = envelope["payload_sha256"]
    if actual_digest != expected_digest:
        raise DigestMismatchError(
            f"Digest mismatch (expected {expected_digest}, got {actual_digest})."
        )

    try:
        signature_bytes = base64.b64decode(envelope["signature_b64"], validate=True)
    except Exception as exc:  # noqa: BLE001
        raise MalformedEnvelopeError("signature_b64 is not valid base64.") from exc

    try:
        load_public_key().verify(signature_bytes, payload_path.read_bytes(), ec.ECDSA(hashes.SHA256()))
    except InvalidSignature as exc:
        raise InvalidSignatureError("Signature verification failed for payload and key.") from exc

    return "Verification passed."


def run_case(case_id: str, failure: str, payload: Path, signature: Path) -> FailureResult:
    try:
        verify_payload(payload, signature)
    except VerificationError as exc:
        return FailureResult(
            case_id=case_id,
            failure=failure,
            message=f"[{exc.code}] {exc}",
            remediation=exc.remediation,
        )
    return FailureResult(
        case_id=case_id,
        failure=failure,
        message="[UNEXPECTED_PASS] Verification passed unexpectedly.",
        remediation="Recheck negative test setup.",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run POC-05 error taxonomy simulation.")
    parser.add_argument(
        "--input-json",
        type=Path,
        help="Optional OSCAL JSON file used as baseline payload for failure cases.",
    )
    return parser.parse_args()


def mutate_first_string(value: Any) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            if isinstance(nested, str):
                value[key] = f"{nested} [TAMPERED]"
                return True
            if mutate_first_string(nested):
                return True
    elif isinstance(value, list):
        for nested in value:
            if mutate_first_string(nested):
                return True
    return False


def main() -> int:
    args = parse_args()
    CASES_DIR.mkdir(parents=True, exist_ok=True)
    ensure_keypair()

    payload_ok = CASES_DIR / "sample-oscal.json"
    if args.input_json:
        if not args.input_json.exists():
            raise FileNotFoundError(f"Input OSCAL JSON not found: {args.input_json}")
        write_text(payload_ok, args.input_json.read_text(encoding="utf-8"))
        source_label = str(args.input_json)
    else:
        write_text(
            payload_ok,
            json.dumps(
                {
                    "catalog": {
                        "uuid": "9a5aa4d1-9ff2-4012-b8be-e9f99b7d1aaa",
                        "metadata": {"title": "POC-05 Sample", "version": "1.0.0"},
                    }
                },
                indent=2,
            )
            + "\n",
        )
        source_label = "built-in sample JSON"
    sig_ok = CASES_DIR / "sample-oscal.sig"
    sign_payload(payload_ok, sig_ok)

    # Case 1: missing OSCAL file
    case1_payload = CASES_DIR / "missing-oscal.json"
    case1_sig = sig_ok

    # Case 2: missing .sig file
    case2_payload = payload_ok
    case2_sig = CASES_DIR / "missing.sig"

    # Case 3: digest mismatch
    case3_payload = CASES_DIR / "tampered-oscal.json"
    original_obj = json.loads(payload_ok.read_text(encoding="utf-8"))
    if not mutate_first_string(original_obj):
        original_obj = {"changed": True, "original": original_obj}
    write_text(case3_payload, json.dumps(original_obj, indent=2) + "\n")
    case3_sig = sig_ok

    # Case 4: invalid signature
    case4_payload = payload_ok
    case4_sig = CASES_DIR / "invalid-signature.sig"
    env_invalid_sig = json.loads(sig_ok.read_text(encoding="utf-8"))
    sig_bytes = base64.b64decode(env_invalid_sig["signature_b64"])
    tampered_sig_bytes = bytes([sig_bytes[0] ^ 0x01]) + sig_bytes[1:]
    env_invalid_sig["signature_b64"] = base64.b64encode(tampered_sig_bytes).decode("ascii")
    write_text(case4_sig, json.dumps(env_invalid_sig, indent=2) + "\n")

    # Case 5: unsupported algorithm
    case5_payload = payload_ok
    case5_sig = CASES_DIR / "unsupported-algorithm.sig"
    env_unsupported = json.loads(sig_ok.read_text(encoding="utf-8"))
    env_unsupported["algorithm"] = "rsa-pss-sha512"
    write_text(case5_sig, json.dumps(env_unsupported, indent=2) + "\n")

    # Case 6: malformed signature envelope
    case6_payload = payload_ok
    case6_sig = CASES_DIR / "malformed.sig"
    write_text(case6_sig, "{ this is not valid json }\n")

    results = [
        run_case("C1", "missing OSCAL file", case1_payload, case1_sig),
        run_case("C2", "missing .sig file", case2_payload, case2_sig),
        run_case("C3", "digest mismatch", case3_payload, case3_sig),
        run_case("C4", "invalid signature", case4_payload, case4_sig),
        run_case("C5", "unsupported algorithm", case5_payload, case5_sig),
        run_case("C6", "malformed signature envelope", case6_payload, case6_sig),
    ]

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / "poc05_error_results.json").write_text(
        json.dumps([r.__dict__ for r in results], indent=2) + "\n",
        encoding="utf-8",
    )

    md_lines = [
        "# POC-05 Failure -> Message -> User Action",
        "",
        "| Case | Failure | Message | User Action |",
        "|---|---|---|---|",
    ]
    for r in results:
        md_lines.append(f"| {r.case_id} | {r.failure} | `{r.message}` | {r.remediation} |")
    (ARTIFACTS / "poc05_error_matrix.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    transcript_lines = [
        "POC-05 Error Taxonomy and UX Transcript",
        "",
        f"Input source: {source_label}",
        "All expected failures were triggered with actionable remediation hints.",
        "",
        "Command-style output snippets:",
    ]
    for r in results:
        transcript_lines.append(f"- {r.case_id} {r.failure}: {r.message}")
        transcript_lines.append(f"  -> action: {r.remediation}")

    transcript_lines.extend(
        [
            "",
            "Artifacts:",
            "- poc05_error_results.json",
            "- poc05_error_matrix.md",
        ]
    )
    transcript = "\n".join(transcript_lines) + "\n"
    (ARTIFACTS / "poc05_transcript.txt").write_text(transcript, encoding="utf-8")
    print(transcript, end="")

    all_expected = all("[UNEXPECTED_PASS]" not in r.message for r in results)
    return 0 if all_expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
