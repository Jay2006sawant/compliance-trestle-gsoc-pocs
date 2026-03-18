# POC-06 Architecture and Hook Map

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
