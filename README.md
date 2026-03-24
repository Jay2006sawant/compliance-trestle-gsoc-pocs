# compliance-trestle GSOC — PoCs

This repository is my **evidence track** for the OSCAL document signing work I
proposed for
[oscal-compass/compliance-trestle](https://github.com/oscal-compass/compliance-trestle),
primarily against:

- [#2037 — trestle support for OSCAL document signing](https://github.com/oscal-compass/compliance-trestle/issues/2037)
- [#2013 — Support JSON Canonicalization Scheme to support cryptographic signing scenarios](https://github.com/oscal-compass/compliance-trestle/issues/2013)

The repository does **not** contain a production implementation inside
`compliance-trestle`. Instead, it contains runnable proofs of concept,
generated artifacts, comparison notes, and proposal-supporting design evidence
that I used to de-risk the final implementation plan.

## What this repository contains

- `POC/` — the main PoC lab, including 12 focused proofs of concept plus a hub
  README, tracker, runner, smoke tests, and generated artifacts
- `SIGNING_ENVELOPE_COMPARISON.md` — detailed trade-off analysis for choosing a
  minimal JSON sidecar over JWS and DSSE/Sigstore for the MVP
- `timeline.md` — placeholder schedule/design planning note for proposal
  support

## PoC coverage

The PoCs cover the major themes from the proposal:

- detached signing and tamper detection
- deterministic canonicalization and digest generation
- signature-envelope design trade-offs
- ECDSA / RSA-PSS compatibility checks
- verification error taxonomy and user-facing remediation
- architecture hook points in existing trestle workflows
- policy rollout modes (`off`, `warn`, `enforce`)
- lifecycle placement of signing in a CI pipeline
- metadata and provenance value
- threat-model and non-goal clarification
- test strategy and coverage planning
- documentation/tutorial usability

## Verification status

I verified the repository from the repo root with:

```bash
python3 POC/run_all_pocs.py
python3 -m unittest POC/test_poc_smoke.py -v
```

At the time of the latest documentation update, all 12 PoC scripts completed
successfully and the smoke tests passed.

## Repository layout

- `POC/README.md` — hub README for the PoC lab
- `POC/INDEX.md` — quick tracker for all PoCs and their evidence
- `POC/run_all_pocs.py` — executes the full PoC suite and writes a verification
  report
- `POC/test_poc_smoke.py` — basic smoke tests for key PoC paths
- `POC/POC_1` … `POC/POC_12` — one focused PoC per topic

## How to use this repository

If you want the fastest overview:

1. Read `POC/INDEX.md`
2. Read `SIGNING_ENVELOPE_COMPARISON.md`
3. Open the individual `POC_x/README.md` files for the evidence relevant to a
   milestone

If you want to reproduce the evidence locally:

```bash
python3 POC/run_all_pocs.py
python3 -m unittest POC/test_poc_smoke.py -v
```

Requires Python 3.10+ and `cryptography` (a local venv is recommended).
