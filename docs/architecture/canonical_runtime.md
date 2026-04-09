# Canonical Runtime

Status: accepted
Confidence: high

## Current baseline
Hyperflow is the current **MVP Core**, **Runtime Shell**, **Reasoning Authority**, **Control Authority**, and **Minimal Orchestration Layer**. This repository is sufficient to explain what Hyperflow is now, how the current runtime works, and which path is canonical.

No new canonical behavior may emerge outside the baseline qualification gate.

## Canonical runtime path
The active package identity is `hyperflow`. The canonical path is:

- parser/control -> `hyperflow.language.command_builder.build_command()`
- baseline action routing -> `hyperflow.language.action_router.route_emoji_actions()`
- MPS / control -> `hyperflow.control/*`
- runtime execution -> `hyperflow.engine.runtime_kernel.run()`
- baseline action execution -> `hyperflow.engine.action_registry.*`
- output contract -> `hyperflow.output.run_payload.serialize_run_payload()`
- persistence / checkpoints -> `hyperflow.memory/*` and `hyperflow.checkpoint/*`

## Public MVP API surface
The canonical MVP app exposes only the runtime-backed endpoints below:

- `GET /v1/health`
- `POST /v1/run`
- `GET /v1/checkpoints`
- `GET /v1/checkpoints/latest`
- `GET /v1/checkpoints/{checkpoint_id}`
- `GET /v1/logs/recent`

The following donor/product routes remain deferred and non-canonical at this stage:

- `DEFERRED metadata surface (removed from canonical API): GET /v1/agents`
- `DEFERRED metadata surface (removed from canonical API): GET /v1/workflows`

## Guardrails
- keep runtime execution singular
- preserve one parser, one orchestrator root, and one runtime shell
- treat framework/platform/worker layers as future layers until promoted explicitly
- treat archive material and generated runtime artifacts as reference/output only, not baseline source truth
- keep generated runtime state out of the committed baseline snapshot
