#!/usr/bin/env python3
"""POC-08 import/assemble pipeline signing decision artifacts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"


def main() -> int:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    decision = {
        "options": [
            {
                "name": "explicit_manual_signing_only",
                "pros": ["Simple mental model", "No implicit side effects"],
                "cons": ["Easy to forget signing", "Inconsistent artifact trust"],
                "risk": "medium",
            },
            {
                "name": "automatic_signing_post_validation",
                "pros": ["Consistent trust baseline", "Low user friction once configured"],
                "cons": ["Needs policy and key management guardrails"],
                "risk": "low",
            },
            {
                "name": "signing_during_assemble_publish_stage",
                "pros": ["Natural release boundary", "Good for CI/CD integration"],
                "cons": ["Intermediate artifacts may remain unsigned"],
                "risk": "medium",
            },
        ],
        "recommended_option": "automatic_signing_post_validation",
        "tradeoff_note": (
            "Best balance of low operational risk and reliable provenance coverage; "
            "manual mode remains available for exceptional workflows."
        ),
    }
    (ARTIFACTS / "poc08_decision.json").write_text(json.dumps(decision, indent=2) + "\n", encoding="utf-8")

    md = """# POC-08 Signing Decision in Artifact Lifecycle

## Option 1: Explicit manual signing only
```mermaid
flowchart LR
  A[Create/Import] --> B[Validate]
  B --> C[User manually runs sign]
  C --> D[Signed artifact]
```

## Option 2: Automatic signing post-validation (recommended)
```mermaid
flowchart LR
  A[Create/Import] --> B[Validate]
  B --> C[Auto-sign on success]
  C --> D[Signed artifact]
```

## Option 3: Sign during assemble/publish stage
```mermaid
flowchart LR
  A[Create/Import] --> B[Intermediate artifacts]
  B --> C[Assemble/Publish]
  C --> D[Sign release artifact]
```

## Recommendation

Start with **automatic signing post-validation** for core workflows.

Why:
- provides consistent trust signal with minimal user burden
- keeps migration to CI/publish-stage signing straightforward
- still allows manual overrides for exceptional cases
"""
    (ARTIFACTS / "poc08_sequence_and_recommendation.md").write_text(md, encoding="utf-8")

    transcript = """POC-08 Import/Assemble Signing Decision Transcript

Recommendation:
- automatic signing post-validation

Reason:
- low-risk, defensible integration point with strong trust consistency

Artifacts:
- poc08_decision.json
- poc08_sequence_and_recommendation.md
"""
    (ARTIFACTS / "poc08_transcript.txt").write_text(transcript, encoding="utf-8")
    print("Generated POC-08 artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
