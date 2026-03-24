# Signing envelope comparison

This note records why I chose a minimal, versioned JSON sidecar as the MVP
envelope for OSCAL signing, while keeping JWS and DSSE/Sigstore as future
interoperability directions.

## Decision summary

For the first implementation, I choose a detached JSON sidecar with explicit
fields such as:

- `trestle_signature_version`
- `algorithm`
- `payload_sha256`
- `signature_b64`
- `metadata`

This is the best MVP fit because it keeps the OSCAL artifact unchanged, is easy
to review in code and documentation, and maps directly to the detached-signature
workflow requested in the upstream issue.

## Options compared

| Option | Strengths | Weaknesses / trade-offs | MVP decision |
| --- | --- | --- | --- |
| Minimal JSON sidecar | Small surface area, easy CLI UX, detached by default, explicit versioning, simple to test | Not a standard interchange format by itself; custom verifier logic is needed | Chosen for MVP |
| JWS | Established IETF standard, good JSON ecosystem familiarity, clear signature semantics | Adds more format complexity than needed for the first OSCAL signing release; detached UX is less natural for this workflow | Deferred |
| DSSE / Sigstore | Strong supply-chain story, supports keyless/OIDC identity, modern CI alignment | Operationally heavier; introduces more moving pieces than needed for the initial JSON + JCS + CLI delivery | Deferred |

## Why JSON sidecar is the right first step

The upstream goals prioritize:

- reproducible verification for OSCAL artifacts
- detached signatures that do not modify the OSCAL file
- clear CLI commands (`trestle sign`, `trestle verify`)
- maintainable implementation and documentation

The JSON sidecar approach satisfies all of these with the least implementation
risk. It also works naturally with the JCS-based digest pipeline:

`parsed OSCAL JSON -> canonical UTF-8 bytes -> SHA-256 digest -> detached sidecar`

This makes the signing and verification story straightforward for both users and
reviewers.

## Why the other options are not the first choice

### JWS

JWS is a valid standard option, but for this project it adds complexity before
the basic OSCAL signing flow is stable. The proposal already has to introduce:

- in-tree JCS canonicalization
- deterministic digest generation
- signature envelope validation
- CLI behavior and failure taxonomy

Adding full JWS semantics in the first iteration would increase the surface area
without clearly improving the core JSON signing MVP.

### DSSE / Sigstore

DSSE and Sigstore are attractive for future CI and supply-chain integrations,
especially when keyless/OIDC identity matters. However, they are a better fit
after the project has a stable JSON signing baseline. For the first delivery,
they would add integration and operational complexity that is not necessary to
meet the core attestation goals of the issue.

## Migration path

The chosen sidecar includes a version field so the design can evolve later.
That means future work can introduce JWS- or DSSE/Sigstore-style envelopes
without silently breaking existing verifiers. In other words:

- start with a simple, detached, reviewable envelope
- stabilize JSON + JCS + CLI behavior
- extend interoperability only after the MVP is proven

## Final conclusion

The minimal JSON sidecar is not chosen because JWS or DSSE/Sigstore are
incorrect. It is chosen because it is the most practical and lowest-risk way to
deliver a correct OSCAL signing MVP that is easy to understand, test, document,
and evolve.
