#!/usr/bin/env python3
"""POC-07 policy mode behavior simulation (off|warn|enforce)."""

from __future__ import annotations

import argparse
import base64
import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
CASES = ARTIFACTS / "cases"


@dataclass
class VerifyStatus:
    ok: bool
    code: str
    message: str


def build_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())
    return private_key, private_key.public_key()


def sign_payload(private_key, payload_path: Path, sig_path: Path) -> None:
    payload = payload_path.read_bytes()
    signature = private_key.sign(payload, ec.ECDSA(hashes.SHA256()))
    envelope = {
        "algorithm": "ecdsa-p256-sha256",
        "payload_sha256": sha256(payload).hexdigest(),
        "signature_b64": base64.b64encode(signature).decode("ascii"),
    }
    sig_path.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")


def verify(public_key, payload_path: Path, sig_path: Path) -> VerifyStatus:
    if not sig_path.exists():
        return VerifyStatus(False, "UNSIGNED", "No detached signature found.")

    envelope = json.loads(sig_path.read_text(encoding="utf-8"))
    digest = sha256(payload_path.read_bytes()).hexdigest()
    if digest != envelope["payload_sha256"]:
        return VerifyStatus(False, "DIGEST_MISMATCH", "Payload digest differs from signature envelope.")

    signature = base64.b64decode(envelope["signature_b64"])
    try:
        public_key.verify(signature, payload_path.read_bytes(), ec.ECDSA(hashes.SHA256()))
    except InvalidSignature:
        return VerifyStatus(False, "INVALID_SIGNATURE", "Cryptographic signature verification failed.")
    return VerifyStatus(True, "VALID", "Signature is valid.")


def decide(mode: str, status: VerifyStatus) -> tuple[str, str]:
    if mode == "off":
        return ("ALLOW", "Signature checks disabled by policy.")
    if mode == "warn":
        if status.ok:
            return ("ALLOW", "Valid signature.")
        return ("ALLOW_WITH_WARNING", f"{status.code}: {status.message}")
    if mode == "enforce":
        if status.ok:
            return ("ALLOW", "Valid signature.")
        return ("BLOCK", f"{status.code}: {status.message}")
    raise ValueError(f"Unsupported mode {mode}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run POC-07 policy mode simulation.")
    parser.add_argument(
        "--input-json",
        type=Path,
        help="Optional OSCAL JSON file used as base payload.",
    )
    return parser.parse_args()


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


def main() -> int:
    args = parse_args()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    CASES.mkdir(parents=True, exist_ok=True)
    private_key, public_key = build_keys()

    if args.input_json:
        if not args.input_json.exists():
            raise FileNotFoundError(f"Input OSCAL JSON not found: {args.input_json}")
        base_payload = json.loads(args.input_json.read_text(encoding="utf-8"))
        source_label = str(args.input_json)
    else:
        base_payload = {
            "catalog": {
                "uuid": "23750e1d-d014-4d16-a1a8-333709e2f707",
                "metadata": {"title": "POC-07", "version": "1.0.0"},
            }
        }
        source_label = "built-in sample JSON"

    signed_valid_path = CASES / "signed-valid.json"
    unsigned_path = CASES / "unsigned.json"
    signed_tampered_path = CASES / "signed-tampered.json"

    signed_valid_path.write_text(json.dumps(base_payload, indent=2) + "\n", encoding="utf-8")
    unsigned_path.write_text(json.dumps(base_payload, indent=2) + "\n", encoding="utf-8")
    signed_tampered_path.write_text(json.dumps(base_payload, indent=2) + "\n", encoding="utf-8")

    signed_valid_sig = CASES / "signed-valid.sig"
    sign_payload(private_key, signed_valid_path, signed_valid_sig)

    signed_tampered_sig = CASES / "signed-tampered.sig"
    sign_payload(private_key, signed_tampered_path, signed_tampered_sig)
    tampered = json.loads(signed_tampered_path.read_text(encoding="utf-8"))
    if not mutate_first_string(tampered):
        tampered = {"changed": True, "original": tampered}
    signed_tampered_path.write_text(json.dumps(tampered, indent=2) + "\n", encoding="utf-8")

    conditions = [
        ("signed_valid", signed_valid_path, signed_valid_sig),
        ("unsigned", unsigned_path, CASES / "unsigned.sig"),
        ("signed_tampered", signed_tampered_path, signed_tampered_sig),
    ]
    modes = ["off", "warn", "enforce"]

    rows = []
    for mode in modes:
        for name, payload, sig in conditions:
            status = verify(public_key, payload, sig)
            behavior, reason = decide(mode, status)
            rows.append(
                {
                    "mode": mode,
                    "condition": name,
                    "behavior": behavior,
                    "reason": reason,
                }
            )

    (ARTIFACTS / "poc07_policy_behavior.json").write_text(
        json.dumps(rows, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# POC-07 Policy Mode Behavior Matrix",
        "",
        "| Mode | File condition | Behavior | Reason |",
        "|---|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r['mode']} | {r['condition']} | {r['behavior']} | {r['reason']} |")
    (ARTIFACTS / "poc07_policy_behavior.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    transcript = [
        "POC-07 Policy Mode Simulation Transcript",
        "",
        f"Input source: {source_label}",
        "Policy behavior is consistent and predictable:",
        "- off: always allow",
        "- warn: allow + warning on unsigned/tampered",
        "- enforce: block unsigned/tampered, allow valid signed",
        "",
        "Artifacts:",
        "- poc07_policy_behavior.json",
        "- poc07_policy_behavior.md",
    ]
    (ARTIFACTS / "poc07_transcript.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
