# Platform Surface

Status: donor-only for future phases
Confidence: high

## Decision

`hyperflow-platform-canonical-1` is a product-surface donor, not a runtime seed.

It may later donate:

- request/response model structure
- `/v1/agents`
- `/v1/workflows`
- inventory / preset concepts
- Android shell

Checkpoint and recent-log endpoints are already absorbed into the canonical MVP runtime because they are runtime-backed observability surfaces, not separate platform identity.

## Evidence

The platform repo has its own backend package root and its own package metadata, which makes it a parallel package identity and a parallel runtime shell.

## Rule

Baseline work must not ingest platform runtime code in a way that creates a second active package root or second execution spine. Platform-owned public routes remain deferred donor/product surface and require an explicit promotion decision before they gain canonical MVP authority.
