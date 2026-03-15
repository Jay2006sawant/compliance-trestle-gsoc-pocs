#!/usr/bin/env python3
"""POC-01 detached signing MVP demo for OSCAL JSON artifacts."""

from __future__ import annotations

import argparse
import base64
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT / "workspace"
SOURCE_JSON = WORKSPACE / "catalogs" / "sample-catalog" / "catalog.json"
ARTIFACTS = ROOT / "artifacts"
KEYS = ROOT / "keys"
PRIVATE_KEY_PATH = KEYS / "poc01-private.pem"
PUBLIC_KEY_PATH = KEYS / "poc01-public.pem"
TRANSCRIPT_PATH = ARTIFACTS / "poc01_transcript.txt"


@dataclass
class VerifyResult:
    ok: bool
    message: str


def ensure_dirs() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    KEYS.mkdir(parents=True, exist_ok=True)


def ensure_source_model() -> None:
    if not SOURCE_JSON.exists():
        raise FileNotFoundError(
            "Missing sample OSCAL JSON. Generate it first with:\n"
            "./venv/bin/python -m trestle init -loc -tr GSOC/POC/POC_1/workspace\n"
            "./venv/bin/python -m trestle create -t catalog -o sample-catalog -x json "
            "-tr GSOC/POC/POC_1/workspace"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run POC-01 detached signing demo.")
    parser.add_argument(
        "--input-json",
        type=Path,
        default=SOURCE_JSON,
        help="Path to OSCAL JSON input (default: generated sample catalog).",
    )
    return parser.parse_args()


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


def digest_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def sign_file(payload_path: Path, sig_path: Path) -> None:
    payload = payload_path.read_bytes()
    digest = sha256(payload).hexdigest()
    private_key = load_private_key()
    signature = private_key.sign(payload, ec.ECDSA(hashes.SHA256()))
    envelope = {
        "algorithm": "ecdsa-p256-sha256",
        "payload_file": payload_path.name,
        "payload_sha256": digest,
        "signature_b64": base64.b64encode(signature).decode("ascii"),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    sig_path.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")


def verify_file(payload_path: Path, sig_path: Path) -> VerifyResult:
    envelope = json.loads(sig_path.read_text(encoding="utf-8"))
    expected_digest = envelope["payload_sha256"]
    actual_digest = digest_file(payload_path)
    if actual_digest != expected_digest:
        return VerifyResult(
            False,
            (
                "Digest mismatch: payload changed after signing "
                f"(expected {expected_digest}, got {actual_digest})"
            ),
        )

    signature = base64.b64decode(envelope["signature_b64"])
    public_key = load_public_key()
    payload = payload_path.read_bytes()
    try:
        public_key.verify(signature, payload, ec.ECDSA(hashes.SHA256()))
    except InvalidSignature:
        return VerifyResult(False, "Invalid signature for payload and signer key.")
    return VerifyResult(True, "Verification passed.")


def make_tampered_copy(source_path: Path, target_path: Path) -> None:
    source_obj = json.loads(source_path.read_text(encoding="utf-8"))

    def mutate_first_string(value: object) -> bool:
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

    if not mutate_first_string(source_obj):
        raise ValueError("Unable to locate a mutable string field for tamper step.")
    target_path.write_text(json.dumps(source_obj, indent=2) + "\n", encoding="utf-8")


def run(input_json: Path) -> int:
    ensure_dirs()
    if input_json == SOURCE_JSON:
        ensure_source_model()
    if not input_json.exists():
        raise FileNotFoundError(f"Input OSCAL JSON not found: {input_json}")
    ensure_keypair()

    base_name = input_json.stem
    original_json = ARTIFACTS / f"{base_name}.original.json"
    tampered_json = ARTIFACTS / f"{base_name}.tampered.json"
    original_sig = ARTIFACTS / f"{base_name}.original.sig"
    tampered_sig = ARTIFACTS / f"{base_name}.tampered.sig"

    shutil.copy2(input_json, original_json)
    sign_file(original_json, original_sig)
    step1 = verify_file(original_json, original_sig)

    make_tampered_copy(original_json, tampered_json)
    step2 = verify_file(tampered_json, original_sig)

    sign_file(tampered_json, tampered_sig)
    step3 = verify_file(tampered_json, tampered_sig)

    lines = [
        "POC-01 Detached Signing MVP Transcript",
        "",
        f"Source OSCAL JSON: {input_json}",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Step 1 - Sign original OSCAL JSON and verify:",
        f"  signature: {original_sig.name}",
        f"  result: {'PASS' if step1.ok else 'FAIL'} - {step1.message}",
        "",
        "Step 2 - Tamper one field and verify with original signature:",
        f"  tampered file: {tampered_json.name}",
        f"  result: {'PASS' if step2.ok else 'FAIL'} - {step2.message}",
        "",
        "Step 3 - Re-sign tampered file and verify again:",
        f"  signature: {tampered_sig.name}",
        f"  result: {'PASS' if step3.ok else 'FAIL'} - {step3.message}",
        "",
        "Evidence files:",
        f"  - {original_json.name}",
        f"  - {tampered_json.name}",
        f"  - {original_sig.name}",
        f"  - {tampered_sig.name}",
    ]
    transcript = "\n".join(lines) + "\n"
    TRANSCRIPT_PATH.write_text(transcript, encoding="utf-8")
    print(transcript, end="")
    return 0 if (step1.ok and (not step2.ok) and step3.ok) else 1


if __name__ == "__main__":
    args = parse_args()
    raise SystemExit(run(args.input_json))
