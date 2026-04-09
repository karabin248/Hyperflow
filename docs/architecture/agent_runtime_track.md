# Hyperflow Agent Runtime Track

Status: candidate next layer  
Classification: Agent runtime candidate

## Baseline dependencies

The Hyperflow v0.2.0 baseline remains canonical underneath this layer:

- Hyperflow = shell
- MPS = state-policy
- EDDE = process contract
- Observer = guardrails
- Fragment = output object
- canonical cycle = `🌈💎🔥🧠🔀⚡`

The agent runtime attaches above the baseline and must execute delegated work through the canonical baseline path:

- `build_command(...)`
- `runtime_kernel.run(...)`

## Proposed next-layer addition

`hyperflow/agent_runtime/*` is the controlled attachment point for:

- agent role specs
- delegation plans
- coordination steps
- baseline-backed worker execution adapters
- agent run records, task traces, and failure-policy records
- agent-run persistence and trace-store comparison tooling
- persistence-backed analysis views and promotion-evaluation utilities
- exportable promotion-review summaries and scoring thresholds
- option generation across roles
- agent-level delegation validation and guardrails

## Scope boundaries

Belongs to baseline:

- parser / command construction
- MPS / EDDE / Observer semantics
- runtime kernel authority
- active mounted MVP API

Belongs to agent runtime:

- role registry above worker metadata
- delegation planning
- multi-step coordination above the baseline shell
- agent-level traces / result envelopes / failure-policy records
- option generation across roles
- delegation validation and coordination guardrails

Stays outside baseline for now:

- mounted `/v1/agents`
- mounted `/v1/workflows`
- queueing / scheduler / distributed worker execution
- platform admin surfaces
- product packaging assumptions

## Guardrails

The agent runtime candidate must preserve baseline authority by design:

- no second runtime spine
- delegated execution must route through the canonical baseline path
- invalid delegation graphs are rejected before execution
- failed delegation paths must emit observable failure-policy records
- option synthesis must remain traceable to delegated task outputs
- direct baseline vs delegated-agent comparisons must stay evidence-backed
- repeated delegated runs must remain comparable over time through agent-layer trace storage
- promotion readiness must be evaluated from persisted evidence rather than narrative claims
- promotion review exports must remain durable enough for decision logging
- agent-level behavior is test-backed before any promotion discussion

## Promotion criteria

Any future promotion closer to baseline relevance requires all of the following:

- useful real delegation behavior
- baseline-backed execution only
- explicit contracts across code, docs, and tests
- explicit option generation, traces, persistence, and failure-policy guardrails
- direct delegated-vs-baseline comparison coverage
- persistence-backed analysis views and promotion-evaluation utilities
- exportable promotion-review summaries and scoring thresholds
- no second runtime spine
- reversible integration


## Framework bridge persistence

Framework agent nodes now delegate through the persisted agent-runtime coordinator rather than calling the baseline adapter directly. This keeps framework execution above the canonical baseline while making framework_run_id, agent-run ids, delegation plan ids, baseline run ids, and selected options observable across framework outputs and persisted agent-runtime traces.


## Framework bridge stability

Framework agent runs now use stable delegation plan ids by agent/task or workflow node scope so repeated framework runs can participate in persisted comparison and promotion review without inventing a second execution authority.
