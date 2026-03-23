#!/usr/bin/env python3
"""Generate POC-06 architecture and hook-map artifacts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"


def write_json_artifact() -> None:
    payload = {
        "objective": "Prove signing design fits trestle write/read architecture.",
        "write_paths": {
            "write_file_action": {
                "entry_points": [
                    "trestle/core/commands/create.py",
                    "trestle/core/commands/import_.py",
                    "trestle/core/commands/split.py",
                    "trestle/core/commands/merge.py",
                    "trestle/core/commands/assemble.py",
                    "trestle/core/commands/add.py",
                    "trestle/core/commands/remove.py",
                    "trestle/core/commands/replicate.py",
                ],
                "core_hook": "trestle/core/models/actions.py::WriteAction.execute",
            },
            "oscal_write": {
                "entry_points": [
                    "trestle/tasks/xlsx_to_oscal_cd.py",
                    "trestle/tasks/xccdf_result_to_oscal_ar.py",
                    "trestle/tasks/osco_result_to_oscal_ar.py",
                    "trestle/core/commands/author/component.py",
                    "trestle/core/commands/author/catalog.py",
                    "trestle/core/commands/author/prof.py",
                    "trestle/core/commands/href.py",
                ],
                "core_hook": "trestle/core/base_model.py::OscalBaseModel.oscal_write",
            },
        },
        "read_and_validate_paths": {
            "read": "trestle/core/base_model.py::OscalBaseModel.oscal_read",
            "validate": [
                "trestle/core/commands/validate.py::ValidateCmd._run",
                "trestle/core/validator.py::Validator.validate",
            ],
            "distributed_load": "trestle/common/model_utils.py::ModelUtils.load_distributed",
        },
        "recommended_mvp_hooks": [
            {
                "hook": "Sign on write",
                "location": "WriteAction.execute",
                "reason": "Covers major CLI write flows that use WriteFileAction.",
            },
            {
                "hook": "Sign on write",
                "location": "OscalBaseModel.oscal_write",
                "reason": "Covers tasks and author flows that bypass WriteFileAction.",
            },
            {
                "hook": "Verify on read",
                "location": "OscalBaseModel.oscal_read",
                "reason": "Central read path used by distributed loader and many validators.",
            },
            {
                "hook": "Verify on validate",
                "location": "validator_factory addition (SignatureValidator)",
                "reason": "Supports policy modes and optional strict enforcement.",
            },
        ],
        "known_gap_paths": [
            {
                "location": "trestle/core/remote/cache.py::FetcherBase.get_oscal",
                "risk": "Uses raw dict loading + parser.parse_dict and can bypass oscal_read verification hook.",
                "mitigation": "Add verification in fetch/cache path or route through oscal_read equivalent.",
            }
        ],
        "success_criteria_check": {
            "no_major_path_left_unsigned_by_design": "PARTIAL PASS - major write/read paths are covered by proposed hooks; remote fetch path requires explicit hook to close bypass.",
        },
    }
    (ARTIFACTS / "poc06_hook_points.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def write_markdown_artifact() -> None:
    content = """# POC-06 Architecture and Hook Map

## Target architecture flows

### Write flow A (CLI write via WriteFileAction)

`cli -> command -> Plan.execute -> WriteFileAction.execute -> WriteAction.execute -> Element.to_json/to_yaml -> file write`

### Write flow B (direct model write via oscal_write)

`cli/task -> model_instance.oscal_write -> serialized bytes/text -> file write`

### Read/validate flow

`cli validate -> ValidateCmd -> Validator.validate -> ModelUtils.load_distributed -> OscalBaseModel.oscal_read`

## Recommended hook points

| Hook | Location | Why |
|---|---|---|
| Sign on write | `trestle/core/models/actions.py::WriteAction.execute` | Captures create/import/split/merge/assemble/add/remove/replicate write path |
| Sign on write | `trestle/core/base_model.py::OscalBaseModel.oscal_write` | Captures tasks/author flows that call model write directly |
| Verify on read | `trestle/core/base_model.py::OscalBaseModel.oscal_read` | Central read point for distributed loading |
| Verify on validate | `trestle/core/validator_factory.py` + new validator | Supports policy-driven signature enforcement in validation workflows |

## Gap analysis

| Potential bypass | Risk | Mitigation |
|---|---|---|
| `trestle/core/remote/cache.py::FetcherBase.get_oscal` | Uses `load_file` + `parser.parse_dict` and may bypass `oscal_read` verification hook | Add verification in cache/fetch path or route through a verification-aware read function |

## POC-06 outcome

- Write/read integration points are identified with concrete files/functions.
- Hook plan is actionable for MVP implementation.
- One notable bypass path is identified with mitigation guidance.
"""
    (ARTIFACTS / "poc06_architecture_hook_map.md").write_text(content, encoding="utf-8")


def write_transcript() -> None:
    transcript = """POC-06 Trestle Workflow Integration Check Transcript

Objective:
- Prove signing design fits trestle write/read architecture.

Findings:
- Two primary write paths exist and both need signing hooks:
  1) WriteAction/WriteFileAction path
  2) OscalBaseModel.oscal_write path
- Read/validate path centers on OscalBaseModel.oscal_read and Validator.validate.
- Remote cache get_oscal path is a known bypass candidate and requires explicit verification coverage.

Success criteria:
- no major path left unsigned by design: PARTIAL PASS
  (major paths covered by hook plan; remote cache path mitigation identified)

Artifacts:
- poc06_hook_points.json
- poc06_architecture_hook_map.md
"""
    (ARTIFACTS / "poc06_transcript.txt").write_text(transcript, encoding="utf-8")


def main() -> int:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    write_json_artifact()
    write_markdown_artifact()
    write_transcript()
    print("Generated POC-06 artifacts in POC/POC_6/artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
