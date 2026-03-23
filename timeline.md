# OSCAL signing proposal timeline

This timeline translates my final proposal into a printable 22-week execution
plan for a large GSoC project.

## Timeline principles

- Milestones 1 to 5 deliver the core JSON signing MVP.
- Milestone 6 captures policy and cross-document follow-on design work.
- I reserve two explicit buffer periods: one before midterm and one before final
  evaluation.
- Those buffer weeks are there for unexpected delays, bug fixing, test
  expansion, review feedback, and documentation cleanup.

## Community bonding

| Phase | Focus | Plan |
| --- | --- | --- |
| Community Bonding | Project alignment and setup | During community bonding, I will review the relevant `compliance-trestle` code paths, re-read issues `#2037` and `#2013`, confirm the MVP scope, validate my local environment, and align naming, CLI, test, and documentation expectations with the project. |

## Phase 1 — Design and core library (Weeks 1–7)

| Week | Milestone | Focus | Plan |
| --- | --- | --- | --- |
| 1 | M1 | Trust model and envelope baseline | I will finalize the signing trust contract, detached sidecar design, JSON-only MVP boundary, and the standards rationale for the initial envelope choice. |
| 2 | M1 -> M2 | Canonicalization handoff | This week focuses on converting the design into an implementation-ready plan for JCS canonicalization, digest generation, module boundaries, and edge-case coverage. |
| 3 | M2.1 | Canonical bytes and digest | I will implement the first working path from parsed OSCAL JSON to canonical UTF-8 bytes to SHA-256 digest, keeping signing and verification on the same path. |
| 4 | M2.1 | RFC 8785 number handling | The main focus this week is ECMAScript-compatible number serialization and validation against RFC 8785 Appendix B, including rejection of non-finite values. |
| 5 | M2.2 | Signing library APIs | During Week 5, I will build signature generation, detached sidecar creation, envelope population, and metadata handling on top of canonical bytes. |
| 6 | M2.3 | Verification library APIs | I will implement ordered verification: file checks, envelope parsing, version/algorithm validation, digest recomputation, mismatch handling, and signature verification. |
| 7 | M2.4 | Key handling and trust baseline | This week I will finish PEM key loading, allow-list behavior, trust-policy hooks, and the MVP boundary for local keys and simple CI secret injection. |

## Phase 2 — Buffer and midterm checkpoint (Weeks 8–9)

| Week | Milestone | Focus | Plan |
| --- | --- | --- | --- |
| 8 | Buffer | Stabilization before midterm | I reserve this week for unexpected delays, refactoring, bug fixing, coverage improvements, and cleanup before the midterm checkpoint. |
| 9 | Midterm | Consolidation and review | Midterm preparation happens here: I will consolidate Milestones 1 and 2, respond to feedback, and make sure the design and implementation are consistent and demonstrable. |

## Phase 3 — CLI and quality gates (Weeks 10–15)

| Week | Milestone | Focus | Plan |
| --- | --- | --- | --- |
| 10 | M3.1 | `trestle sign` | In Week 10, I will implement `trestle sign`, including argument parsing, key loading, sidecar defaults, detached envelope writing, and exit behavior. |
| 11 | M3.2 | `trestle verify` | This week I will implement `trestle verify`, covering sidecar lookup, public-key verification, digest-first failure behavior, trust checks, and user-facing error reporting. |
| 12 | M3.3 | CLI integration | I will wire the new commands into the trestle CLI, align them with `CommandBase` patterns, and improve command ergonomics and help text. |
| 13 | M3.4 | Lifecycle and CI integration | The focus here is the intended workflow order: generate, validate, sign, publish, and verify. I will also align the command behavior with the CI example in the proposal. |
| 14 | M4.1 | Test matrix expansion | Week 14 is dedicated to unit and integration tests for canonicalization, signing, verification, negative cases, and CLI behavior. |
| 15 | M4.2–M4.3 | Coverage and golden gates | I will finish the quality gate by wiring scoped coverage expectations and RFC 8785 Appendix B golden tests into automated validation. |

## Phase 4 — Documentation and final MVP hardening (Weeks 16–19)

| Week | Milestone | Focus | Plan |
| --- | --- | --- | --- |
| 16 | M5.1–M5.2 | Tutorial and API docs | This week I will write the end-to-end tutorial and document the reusable public APIs, including typed exceptions and expected verification behavior. |
| 17 | M5.3–M5.4 | Operations and alignment docs | The work here covers rotation, revocation, allow-lists, CI usage, non-goals, and the compliance-alignment explanation for integrity, provenance, and supply-chain expectations. |
| 18 | Buffer | Stabilization before final evaluation | I reserve this as a second buffer for unexpected defects, integration issues, mentor feedback, documentation gaps, and final cleanup before the end-stage evaluation window. |
| 19 | Final MVP | Hardening and final review prep | In Week 19, I will prepare the stable JSON signing MVP for final review, verify that implemented scope matches the proposal, and tighten tests and docs where needed. |

## Phase 5 — Extended design work (Weeks 20–22)

| Week | Milestone | Focus | Plan |
| --- | --- | --- | --- |
| 20 | M6.1 | Policy integration design | This week focuses on validation-layer policy design: `off / warn / enforce`, rejection semantics, and expiration/revalidation windows at the design level. |
| 21 | M6.3 | Cross-document ADR | I will complete the committed ADR/design note for manifest-based cross-document integrity, including URI rules, digest pinning, and verification order. |
| 22 | M6.2 / Closeout | Interoperability direction and final polish | The last week is reserved for final polish and documenting future interoperability directions such as Sigstore/DSSE evolution from the versioned sidecar model. |

## Final note

This schedule is intentionally structured so the JSON signing MVP remains the
non-negotiable outcome. The buffer periods reduce delivery risk, and the final
phase captures advanced design work without putting the core implementation at
risk.
