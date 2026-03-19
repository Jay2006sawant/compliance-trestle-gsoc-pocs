# POC-08 Signing Decision in Artifact Lifecycle

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
