# Agent Runtime Delegation Profiles

This document defines the current **delegation-policy profiles** for `hyperflow/agent_runtime/*`.

It applies to the **agent-runtime layer only**.
It uses **MPS-like operating modes** to shape agent coordination, but it must not redefine baseline state-policy semantics.
It does **not** route canonical `/v1/run` through the agent runtime.

## Purpose

Delegation profiles make coordination more controllable by declaring:
- which roles the coordinator may delegate to
- which roles may generate options
- whether research is required before option generation
- whether reporting is required after option selection
- whether a task may override the profile's preferred option behavior

These profiles are runtime controls above the baseline. They are not a second MPS layer.

## Required fields

Each profile includes:
- `id`
- `mode`
- `description`
- `allowed_delegate_roles`
- `option_roles`
- `classification`

## Operational fields

The current agent-runtime layer also requires:
- `require_research`
- `require_reporting`
- `allow_preferred_option_override`
- `default_preferred_option_role`
- `max_option_roles`
- `relationship_to_baseline`

## Current built-in profiles

### `observe`
- mode: `observe`
- evidence first
- only `reasoning` may produce an option
- task-level preferred overrides are not allowed
- intended for conservative, narrow coordination

### `coordinate`
- mode: `coordinate`
- evidence first
- `reasoning` and `tools` may both produce options
- task-level preferred overrides are allowed
- intended as the balanced default profile

### `amplify`
- mode: `amplify`
- evidence first
- `reasoning` and `tools` may both produce options
- defaults to a `tools` preference when the task gives no explicit preference
- intended for broader but still controlled comparison

### `return_to_core`
- mode: `return_to_core`
- evidence first
- only `reasoning` may produce an option
- task-level preferred overrides are not allowed
- intended for conservative return-to-core behavior

## Guardrails

Delegation profiles must satisfy all of the following:
- they must attach above the baseline
- they must not use platform or product classifications
- their `option_roles` must be a subset of `allowed_delegate_roles`
- required research/reporting roles must actually be allowed
- `default_preferred_option_role` must be one of the declared `option_roles`
- `max_option_roles`, when present, must be positive

## Runtime behavior

When a task runs, the agent runtime resolves one profile and records it under:
- `result["delegation_profile"]`
- `agent_runtime.policy_runs`
- handoff fragment metadata
- task start / completion trace payloads

If a task requests option roles outside the active profile, the runtime rejects the task with a `DelegationError`.

## Boundary statement

Delegation profiles are a controllable extension surface for the agent-runtime layer.

They remain:
- an **agent runtime candidate**
- reversible
- outside canonical baseline authority
- separate from baseline MPS semantics
