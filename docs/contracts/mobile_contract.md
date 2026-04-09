# Mobile Contract

Status: deferred donor mapping
Confidence: medium

## Current state

There is no absorbed mobile contract in the canonical `hyperflow` runtime repo yet.

## Donor source

Potential donor:

- `hyperflow-platform-canonical-1`
- backend contracts and Android-facing API models

## PR-01 decision

Document only. Do not import mobile-specific API models or Android wiring yet.

## Future direction

When mobile-facing contracts are absorbed, they must map into the canonical `hyperflow` API surface rather than preserve a second package identity.


## Imported Android shell
The current Android shell is a file-complete UI donor under `apps/android/`. It is intentionally decoupled from auth, worker execution, and any parallel `hyperflow_platform` backend namespace.
