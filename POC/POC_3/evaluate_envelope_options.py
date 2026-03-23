#!/usr/bin/env python3
"""POC-03 signature envelope design comparison."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"


@dataclass(frozen=True)
class Criterion:
    name: str
    weight: int
    why: str


@dataclass(frozen=True)
class Option:
    name: str
    scores: dict[str, int]
    notes: str


def main() -> int:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    criteria = [
        Criterion(
            name="Compatibility with current trestle code",
            weight=4,
            why="Lower change risk helps deliver a working MVP quickly.",
        ),
        Criterion(
            name="Migration complexity",
            weight=3,
            why="We need an approach that can evolve without rewriting everything.",
        ),
        Criterion(
            name="Interoperability",
            weight=4,
            why="Cross-tool verification and ecosystem alignment are long-term goals.",
        ),
        Criterion(
            name="Metadata and provenance support",
            weight=3,
            why="Auditability and traceability matter for compliance workflows.",
        ),
    ]

    options = [
        Option(
            name="Custom minimal detached envelope",
            scores={
                "Compatibility with current trestle code": 5,
                "Migration complexity": 5,
                "Interoperability": 2,
                "Metadata and provenance support": 3,
            },
            notes="Fastest to implement; maps directly to POC-01 detached .sig flow.",
        ),
        Option(
            name="DSSE-style envelope",
            scores={
                "Compatibility with current trestle code": 3,
                "Migration complexity": 2,
                "Interoperability": 5,
                "Metadata and provenance support": 4,
            },
            notes="Strong ecosystem fit for supply chain attestations and provenance.",
        ),
        Option(
            name="JWS-style envelope",
            scores={
                "Compatibility with current trestle code": 2,
                "Migration complexity": 2,
                "Interoperability": 4,
                "Metadata and provenance support": 4,
            },
            notes="Good standards story, but extra JOSE complexity for early MVP.",
        ),
    ]

    # Weighted scores
    weighted_rows = []
    for option in options:
        total = sum(
            option.scores[c.name] * c.weight
            for c in criteria
        )
        weighted_rows.append((option, total))
    weighted_rows.sort(key=lambda row: row[1], reverse=True)

    selected = weighted_rows[0][0]

    matrix = {
        "criteria": [c.__dict__ for c in criteria],
        "options": [
            {
                "name": option.name,
                "scores": option.scores,
                "weighted_total": total,
                "notes": option.notes,
            }
            for option, total in weighted_rows
        ],
        "selected_baseline": selected.name,
        "migration_path": [
            "MVP: custom detached envelope with payload hash, algorithm, and signature bytes.",
            "Near-term: add explicit provenance fields (tool version, signer id, timestamp, build id).",
            "Phase 2: add DSSE-compatible schema adapter and dual-emit mode.",
            "Phase 3: default to DSSE style while maintaining backward verification for MVP signatures.",
        ],
    }
    (ARTIFACTS / "poc03_decision_matrix.json").write_text(
        json.dumps(matrix, indent=2) + "\n", encoding="utf-8"
    )

    md_lines = [
        "# POC-03 Signature Envelope Decision Matrix",
        "",
        "## Criteria and weights",
        "",
        "| Criterion | Weight | Why it matters |",
        "|---|---:|---|",
    ]
    for c in criteria:
        md_lines.append(f"| {c.name} | {c.weight} | {c.why} |")

    md_lines.extend(
        [
            "",
            "## Option scoring",
            "",
            "| Option | Compatibility (x4) | Migration (x3) | Interop (x4) | Metadata (x3) | Weighted total |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for option, total in weighted_rows:
        md_lines.append(
            "| "
            f"{option.name} | "
            f"{option.scores['Compatibility with current trestle code']} | "
            f"{option.scores['Migration complexity']} | "
            f"{option.scores['Interoperability']} | "
            f"{option.scores['Metadata and provenance support']} | "
            f"{total} |"
        )

    md_lines.extend(
        [
            "",
            "## Recommendation",
            "",
            f"Selected baseline for MVP: **{selected.name}**",
            "",
            "Rationale:",
            "- Delivers working value quickly with low integration risk.",
            "- Preserves a clear migration path to DSSE as interoperability needs increase.",
            "",
            "## Migration path to DSSE/Sigstore",
            "",
            "1. Keep detached signature verification stable for MVP users.",
            "2. Expand metadata fields to capture provenance context.",
            "3. Introduce DSSE-compatible envelope adapter and validation mode.",
            "4. Add Sigstore-oriented flow in a future phase (keyless/certificate-based trust model).",
        ]
    )

    (ARTIFACTS / "poc03_decision_matrix.md").write_text(
        "\n".join(md_lines) + "\n", encoding="utf-8"
    )

    transcript = "\n".join(
        [
            "POC-03 Signature Envelope Design Comparison Transcript",
            "",
            f"Selected baseline: {selected.name}",
            "Decision confidence: clear MVP-first recommendation with explicit migration path.",
            "",
            "Output files:",
            "- poc03_decision_matrix.json",
            "- poc03_decision_matrix.md",
        ]
    ) + "\n"
    (ARTIFACTS / "poc03_transcript.txt").write_text(transcript, encoding="utf-8")
    print(transcript, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
