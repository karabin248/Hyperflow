# Agent Runtime Worker Contracts

This document defines the current worker-execution contract for `hyperflow/agent_runtime/*`.

It applies to the **agent-runtime layer only**.
It does **not** redefine baseline worker semantics and does **not** route canonical `/v1/run` through the agent runtime.

## Required fields

Each worker contract includes:
- `id`
- `role`
- `description`
- `input_schema`
- `output_schema`
- `classification`

## Operational fields

The current agent-runtime layer also requires explicit operational descriptors:
- `time_budget_ms`
- `failure_modes`

### `time_budget_ms`
- optional positive integer
- expresses the runtime budget for a worker in milliseconds
- is enforced by the agent-runtime execution layer after worker execution completes
- must not be treated as a baseline runtime contract

### `failure_modes`
Current supported values:
- `handler_exception`
- `invalid_output`
- `time_budget_exceeded`

These values are used to:
- document expected worker failure behavior
- record observable runtime failures
- keep delegation and coordination failures inspectable

## Runtime behavior

When a worker runs, the agent runtime:
- validates input contracts
- records declared `time_budget_ms` and `failure_modes`
- executes the worker handler
- records a failure if the handler raises
- records a failure if output validation fails
- records a failure if the worker exceeds `time_budget_ms`

Failures are stored under `agent_runtime.failures` and traced as `role.failed` events.

## Boundary statement

This contract exists to make worker execution more operationally real above the canonical baseline.

It remains:
- an agent-runtime candidate surface
- reversible
- outside canonical baseline authority


## Retry policy descriptors

Worker contracts may declare an explicit `retry_policy` for agent-runtime execution only.

Retry policy fields:
- `max_attempts`
- `retry_on`
- `backoff_ms`

Scope rules:
- retry behavior is opt-in
- retry behavior remains inside `hyperflow.agent_runtime`
- retry policy does not redefine canonical baseline execution semantics
- retry policy must be reversible and test-backed
