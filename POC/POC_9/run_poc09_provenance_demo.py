#!/usr/bin/env python3
"""POC-09 provenance metadata usefulness demo."""

from __future__ import annotations

import base64
import json
import subprocess
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"


def git_commit_short() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT.parents[2], text=True)
        return out.strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def sign_with_metadata(payload: dict, signer_name: str, build_id: str, model_type: str) -> dict:
    private_key = ec.generate_private_key(ec.SECP256R1())
    payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
    sig = private_key.sign(payload_bytes, ec.ECDSA(hashes.SHA256()))
    return {
        "algorithm": "ecdsa-p256-sha256",
        "payload_sha256": sha256(payload_bytes).hexdigest(),
        "signature_b64": base64.b64encode(sig).decode("ascii"),
        "metadata": {
            "tool_name": "trestle-poc",
            "tool_version": "0.1.0",
            "model_type": model_type,
            "signer_identity": signer_name,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "git_commit": git_commit_short(),
            "build_id": build_id,
        },
    }


def main() -> int:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    payload_a = {"catalog": {"uuid": "aaa", "metadata": {"title": "artifact-A", "version": "1.0.0"}}}
    payload_b = {"catalog": {"uuid": "bbb", "metadata": {"title": "artifact-B", "version": "1.1.0"}}}

    env_a = sign_with_metadata(payload_a, signer_name="alice@example.com", build_id="build-20260319-001", model_type="catalog")
    env_b = sign_with_metadata(payload_b, signer_name="bob@example.com", build_id="build-20260319-042", model_type="catalog")

    (ARTIFACTS / "artifact_a.envelope.json").write_text(json.dumps(env_a, indent=2) + "\n", encoding="utf-8")
    (ARTIFACTS / "artifact_b.envelope.json").write_text(json.dumps(env_b, indent=2) + "\n", encoding="utf-8")

    walkthrough = """# POC-09 Provenance Walkthrough

## Scenario

Two artifacts are both cryptographically signed, but an auditor needs traceability:
- who signed each artifact
- when it was signed
- which tool/build produced it
- which source revision produced it

## How metadata helps

- `signer_identity` distinguishes signer ownership and accountability.
- `timestamp_utc` supports timeline reconstruction during incident review.
- `tool_name` + `tool_version` clarify verifier compatibility and reproducibility.
- `build_id` links artifact to CI/CD execution evidence.
- `git_commit` connects artifact to exact source state.

## Auditor mini-check

1. Compare `artifact_a.envelope.json` and `artifact_b.envelope.json`.
2. Observe different signer/build metadata.
3. Use `git_commit` + `build_id` to retrieve corresponding pipeline logs.
4. Confirm whether provenance aligns with release policy.
"""
    (ARTIFACTS / "poc09_audit_walkthrough.md").write_text(walkthrough, encoding="utf-8")

    transcript = """POC-09 Provenance Metadata Transcript

Result:
- Metadata materially improves auditability and root-cause tracing.

Artifacts:
- artifact_a.envelope.json
- artifact_b.envelope.json
- poc09_audit_walkthrough.md
"""
    (ARTIFACTS / "poc09_transcript.txt").write_text(transcript, encoding="utf-8")
    print("Generated POC-09 artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
