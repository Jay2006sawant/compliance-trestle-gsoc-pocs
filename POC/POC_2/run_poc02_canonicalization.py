#!/usr/bin/env python3
"""POC-02 canonicalization determinism proof for JSON digests."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"


@dataclass
class CaseResult:
    case_id: str
    semantic_group: str
    raw_sha256: str
    canonical_sha256: str


def canonicalize_profile(value: Any) -> bytes:
    """Canonicalization profile used for this PoC.

    Profile:
    - parse JSON into Python object
    - emit compact JSON with lexicographically sorted keys
    - UTF-8 bytes for digest

    Note: This is a practical deterministic profile, not full RFC 8785.
    """
    normalized = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return normalized.encode("utf-8")


def hash_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def hash_bytes(payload: bytes) -> str:
    return sha256(payload).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run POC-02 canonicalization proof.")
    parser.add_argument(
        "--input-json",
        type=Path,
        help="Optional real OSCAL JSON file to use as semantic baseline.",
    )
    return parser.parse_args()


def mutate_first_string(value: Any) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            if isinstance(nested, str):
                value[key] = f"{nested} [CHANGED]"
                return True
            if mutate_first_string(nested):
                return True
    elif isinstance(value, list):
        for nested in value:
            if mutate_first_string(nested):
                return True
    return False


def build_inputs(input_json: Path | None) -> tuple[list[tuple[str, str, str]], str]:
    if input_json is None:
        canonical_semantics_a = {
            "catalog": {
                "uuid": "11111111-2222-3333-4444-555555555555",
                "metadata": {
                    "title": "Canonicalization demo",
                    "version": "1.0.0",
                    "last-modified": "2026-03-19T00:00:00Z",
                },
                "controls": [{"id": "ac-1", "title": "Access control policy"}],
            }
        }
    else:
        canonical_semantics_a = json.loads(input_json.read_text(encoding="utf-8"))

    variant_a_pretty = json.dumps(canonical_semantics_a, indent=2)
    variant_a_compact = json.dumps(canonical_semantics_a, separators=(",", ":"))
    variant_a_sorted = json.dumps(canonical_semantics_a, sort_keys=True, indent=1)

    canonical_semantics_b = json.loads(json.dumps(canonical_semantics_a))
    if not mutate_first_string(canonical_semantics_b):
        canonical_semantics_b = {"changed": True, "original": canonical_semantics_a}
    variant_b_changed_value = json.dumps(canonical_semantics_b, indent=4)

    inputs = [
        ("A_pretty", "A", variant_a_pretty),
        ("A_compact", "A", variant_a_compact),
        ("A_sorted", "A", variant_a_sorted),
        ("B_changed_semantic_value", "B", variant_b_changed_value),
    ]
    source = str(input_json) if input_json else "built-in sample JSON"
    return inputs, source


def main() -> int:
    args = parse_args()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    if args.input_json and not args.input_json.exists():
        raise FileNotFoundError(f"Input OSCAL JSON not found: {args.input_json}")
    inputs, source_label = build_inputs(args.input_json)

    results: list[CaseResult] = []
    for case_id, semantic_group, payload in inputs:
        parsed = json.loads(payload)
        results.append(
            CaseResult(
                case_id=case_id,
                semantic_group=semantic_group,
                raw_sha256=hash_text(payload),
                canonical_sha256=hash_bytes(canonicalize_profile(parsed)),
            )
        )

    json_payload = {
        "canonicalization_profile": "json.dumps(sort_keys=True,separators=(',',':'))",
        "results": [r.__dict__ for r in results],
    }
    (ARTIFACTS / "poc02_digest_results.json").write_text(
        json.dumps(json_payload, indent=2) + "\n", encoding="utf-8"
    )

    md_lines = [
        "# POC-02 Digest Comparison Table",
        "",
        "| Case | Semantic Group | Raw SHA-256 | Canonical SHA-256 |",
        "|---|---|---|---|",
    ]
    for r in results:
        md_lines.append(
            f"| {r.case_id} | {r.semantic_group} | `{r.raw_sha256}` | `{r.canonical_sha256}` |"
        )
    md_lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Group A cases represent the same semantic object with different formatting/key order.",
            "- Canonical digests for Group A must match.",
            "- Group B changes a semantic value and must produce a different canonical digest.",
        ]
    )
    (ARTIFACTS / "poc02_digest_table.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    digest_a = {r.canonical_sha256 for r in results if r.semantic_group == "A"}
    digest_b = {r.canonical_sha256 for r in results if r.semantic_group == "B"}
    same_semantics_match = len(digest_a) == 1
    changed_semantics_different = digest_a.isdisjoint(digest_b)

    transcript_lines = [
        "POC-02 Canonicalization Determinism Transcript",
        "",
        f"Input source: {source_label}",
        f"same semantic object -> same digest: {'PASS' if same_semantics_match else 'FAIL'}",
        f"changed semantic value -> different digest: {'PASS' if changed_semantics_different else 'FAIL'}",
        "",
        "Output files:",
        f"- {(ARTIFACTS / 'poc02_digest_results.json').name}",
        f"- {(ARTIFACTS / 'poc02_digest_table.md').name}",
    ]
    transcript = "\n".join(transcript_lines) + "\n"
    (ARTIFACTS / "poc02_transcript.txt").write_text(transcript, encoding="utf-8")
    print(transcript, end="")

    return 0 if same_semantics_match and changed_semantics_different else 1


if __name__ == "__main__":
    raise SystemExit(main())
