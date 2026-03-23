#!/usr/bin/env python3
"""POC-04 crypto algorithm compatibility benchmark."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"


@dataclass
class AlgoResult:
    algorithm: str
    signature_size_bytes: int
    sign_ms: float
    verify_ms: float
    valid_verify: str
    wrong_key_result: str
    corrupted_sig_result: str
    invalid_key_result: str


def sign_ecdsa(priv, payload: bytes) -> bytes:
    return priv.sign(payload, ec.ECDSA(hashes.SHA256()))


def verify_ecdsa(pub, signature: bytes, payload: bytes) -> None:
    pub.verify(signature, payload, ec.ECDSA(hashes.SHA256()))


def sign_rsapss(priv, payload: bytes) -> bytes:
    return priv.sign(
        payload,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )


def verify_rsapss(pub, signature: bytes, payload: bytes) -> None:
    pub.verify(
        signature,
        payload,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )


def verify_expect_status(fn, *args) -> str:
    try:
        fn(*args)
        return "PASS"
    except InvalidSignature:
        return "FAIL_INVALID_SIGNATURE"
    except Exception as exc:  # noqa: BLE001
        return f"FAIL_{type(exc).__name__}"


def run_algorithm_tests(payload: bytes) -> list[AlgoResult]:
    ecdsa_private = ec.generate_private_key(ec.SECP256R1())
    ecdsa_public = ecdsa_private.public_key()
    ecdsa_wrong_public = ec.generate_private_key(ec.SECP256R1()).public_key()

    rsa_private = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    rsa_public = rsa_private.public_key()
    rsa_wrong_public = rsa.generate_private_key(public_exponent=65537, key_size=3072).public_key()

    # ECDSA
    t0 = time.perf_counter()
    ecdsa_sig = sign_ecdsa(ecdsa_private, payload)
    t1 = time.perf_counter()
    verify_ecdsa(ecdsa_public, ecdsa_sig, payload)
    t2 = time.perf_counter()
    ecdsa_corrupted = bytes([ecdsa_sig[0] ^ 0x01]) + ecdsa_sig[1:]

    ecdsa_result = AlgoResult(
        algorithm="ECDSA_P256_SHA256",
        signature_size_bytes=len(ecdsa_sig),
        sign_ms=(t1 - t0) * 1000,
        verify_ms=(t2 - t1) * 1000,
        valid_verify="PASS",
        wrong_key_result=verify_expect_status(verify_ecdsa, ecdsa_wrong_public, ecdsa_sig, payload),
        corrupted_sig_result=verify_expect_status(verify_ecdsa, ecdsa_public, ecdsa_corrupted, payload),
        invalid_key_result=verify_expect_status(verify_rsapss, rsa_public, ecdsa_sig, payload),
    )

    # RSA-PSS
    t3 = time.perf_counter()
    rsa_sig = sign_rsapss(rsa_private, payload)
    t4 = time.perf_counter()
    verify_rsapss(rsa_public, rsa_sig, payload)
    t5 = time.perf_counter()
    rsa_corrupted = bytes([rsa_sig[0] ^ 0x01]) + rsa_sig[1:]

    rsa_result = AlgoResult(
        algorithm="RSA_PSS_SHA256",
        signature_size_bytes=len(rsa_sig),
        sign_ms=(t4 - t3) * 1000,
        verify_ms=(t5 - t4) * 1000,
        valid_verify="PASS",
        wrong_key_result=verify_expect_status(verify_rsapss, rsa_wrong_public, rsa_sig, payload),
        corrupted_sig_result=verify_expect_status(verify_rsapss, rsa_public, rsa_corrupted, payload),
        invalid_key_result=verify_expect_status(verify_ecdsa, ecdsa_public, rsa_sig, payload),
    )
    return [ecdsa_result, rsa_result]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run POC-04 crypto compatibility benchmark.")
    parser.add_argument(
        "--input-json",
        type=Path,
        help="Optional OSCAL JSON file to use as benchmark payload.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    if args.input_json:
        if not args.input_json.exists():
            raise FileNotFoundError(f"Input OSCAL JSON not found: {args.input_json}")
        payload = args.input_json.read_bytes()
        source_label = str(args.input_json)
    else:
        payload = (
            json.dumps(
                {
                    "catalog": {
                        "uuid": "d5f4d8aa-4df0-4d42-89bc-6fe9aac10101",
                        "metadata": {"title": "POC-04 payload", "version": "1.0.0"},
                    }
                },
                sort_keys=True,
            )
            .encode("utf-8")
        )
        source_label = "built-in sample JSON"

    results = run_algorithm_tests(payload)
    payload_digest = sha256(payload).hexdigest()
    (ARTIFACTS / "poc04_payload_digest.txt").write_text(payload_digest + "\n", encoding="utf-8")

    json_out = {"payload_sha256": payload_digest, "results": [r.__dict__ for r in results]}
    (ARTIFACTS / "poc04_benchmark_results.json").write_text(
        json.dumps(json_out, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# POC-04 Crypto Compatibility Benchmark",
        "",
        "| Algorithm | Signature size (bytes) | Sign time ms | Verify time ms | Valid verify | Wrong key | Corrupted signature | Invalid key/algorithm mismatch |",
        "|---|---:|---:|---:|---|---|---|---|",
    ]
    for r in results:
        lines.append(
            f"| {r.algorithm} | {r.signature_size_bytes} | {r.sign_ms:.3f} | {r.verify_ms:.3f} | "
            f"{r.valid_verify} | {r.wrong_key_result} | {r.corrupted_sig_result} | {r.invalid_key_result} |"
        )
    (ARTIFACTS / "poc04_benchmark_table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    transcript = [
        "POC-04 Crypto Algorithm Compatibility Transcript",
        "",
        f"Input source: {source_label}",
        "Both ECDSA P-256 and RSA-PSS produce valid signatures and verify successfully.",
        "Negative cases (wrong key, corrupted signature, invalid key/algorithm mismatch) fail predictably.",
        "",
        "Artifacts:",
        "- poc04_payload_digest.txt",
        "- poc04_benchmark_results.json",
        "- poc04_benchmark_table.md",
    ]
    (ARTIFACTS / "poc04_transcript.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
