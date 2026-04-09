# Authority Map

Status: canonical
Confidence: high

## Source-of-truth hierarchy

Use this order when authorities conflict:

1. Implemented runtime behavior
2. Canonical runtime docs
3. Tests
4. Patch summaries / decision logs
5. README / notes / exploratory discussions
6. Raw archived conversation history

## Runtime spine

Canonical files and areas:

- `hyperflow/interface/cli.py`
- `hyperflow/__main__.py`
- `hyperflow/api/edde_api.py`
- `hyperflow/language/*`
- `hyperflow/control/*`
- `hyperflow/engine/*`
- `hyperflow/output/*`
- `hyperflow/memory/*`
- `hyperflow/checkpoint/*`

## Baseline authority

Hyperflow baseline is the runtime shell, reasoning authority, and control authority.
Parser/control authority stays baseline-owned.
Baseline action routing stays baseline-owned.
MPS state-policy authority stays baseline-owned.
Output contract authority stays baseline-owned.
Baseline action execution helpers stay baseline-owned.
No new canonical behavior may emerge outside the baseline qualification gate.

The canonical public MVP API is runtime-backed only:

- `GET /v1/health`
- `POST /v1/run`
- `GET /v1/checkpoints`
- `GET /v1/checkpoints/latest`
- `GET /v1/checkpoints/{checkpoint_id}`
- `GET /v1/logs/recent`

Deferred donor/product surface:

- `DEFERRED metadata surface (removed from canonical API): GET /v1/agents`
- `DEFERRED metadata surface (removed from canonical API): GET /v1/workflows`

## Labels

Important decisions should be labeled as one of:

- Canonical
- Confirmed
- Inferred
- Deprecated
- Experimental

## Guardrails

- keep runtime execution path singular
- preserve CLI / API entry → command construction → runtime_kernel.run() → output / persistence
- do not create a second parser, CLI authority, or orchestration spine
- keep core trace / core checkpoint truth stays baseline-owned
- do not let framework or agent-runtime become a checkpoint or observability truth path for baseline runs
- treat committed runtime artifacts as generated output, not source truth
- treat archive material as reference-only, not active runtime authority

## Framework and platform status

- `hyperflow/framework/*` is core-support / extension-support, not the canonical `/v1/run` execution spine
- `hyperflow/platform/*` is future platform/product support, not canonical runtime or public API authority
- `hyperflow/platform/workers/*` remains metadata-only and must not be treated as a second worker runtime
- framework/platform surfaces require an explicit promotion decision before gaining canonical authority

## Dispatch boundary rule (enforced)

`hyperflow/engine/dispatch.py` and `hyperflow/engine/registry.py` MUST NOT import
`hyperflow.framework.runtime` or call `create_operational_framework()`.

Handler resolution for tools and workers flows through `engine.registry` only:
- framework and platform layers **register** handlers into `engine.registry` at init time
- dispatch is a **pure consumer** of that registry
- the dependency direction is always: `framework → engine.registry ← dispatch`

This is enforced by `test_runtime_authority_boundaries.py` and
`tests/contracts/test_dispatch_purity*.py`.
