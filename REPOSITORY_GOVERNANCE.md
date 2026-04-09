# Repository Governance

This document defines how Hyperflow keeps one canonical runtime spine while allowing clearly demoted future layers and donor-reference material.

## 1) Active Runtime Spine
Active implementation truth lives in:
- `hyperflow/interface/*`
- `hyperflow/language/*`
- `hyperflow/control/*`
- `hyperflow/engine/*`
- `hyperflow/output/*`
- `hyperflow/memory/*`
- `hyperflow/checkpoint/*`
- `hyperflow/api/*`

No merge may introduce a second top-level parser, orchestrator, or runtime shell.

## 2) Baseline identity
Hyperflow baseline is explicitly defined as:
- **MVP Core**
- **Runtime Shell**
- **Minimal Orchestration Layer**
- **Reasoning Authority**
- **Control Authority**

No new canonical behavior may emerge outside the baseline qualification gate.

Baseline work should mainly harden, validate, align, freeze, clean, document, guard, or minimally patch the current runtime.

## 3) Future Layer policy
Future layers may exist in the repo, but they do not define canonical runtime behavior unless promoted explicitly:
- `hyperflow/framework/*`
- `hyperflow/agent_runtime/*`
- `hyperflow/platform/*`
- `hyperflow/platform/workers/*`
- `experimental/`
- `archive/`

Allowed donor imports:
- contracts
- schemas
- tools
- validation/reporting
- data fixtures
- API route ideas
- deploy manifests

Disallowed without explicit bridge work:
- alternate CLI shells
- alternate parsers
- alternate orchestrators
- duplicate registries/bootstrap layers
- full agent runtime promotion
- uncontrolled platform/product expansion

## 4) Required metadata for durable decisions
Important changes should record:
- what changed
- why
- classification
- validation result
- canonical vs inferred vs deprecated vs experimental status

## 5) Canonical references
- `README.md`
- `docs/README.md`
- `docs/architecture/canonical_runtime.md`
- `docs/architecture/canonical_core.md`
- `docs/architecture/definition_of_done.md`
- `docs/architecture/authority_map.md`
- `docs/architecture/merge_decisions.md`
- `docs/contracts/runtime_contract.md`
- `docs/contracts/api_contract.md`
- `core/CANONICAL_RUNTIME_SURFACE.md`
- `core/BASELINE_ACCEPTANCE.md`
- `core/MVP_RUNTIME_FREEZE.md`
- `core/RC_RELEASE_CHECKLIST.md`

## 6) MVP supported surface
The MVP release promise is limited to:
- `hyperflow/interface/cli.py`
- `hyperflow/api/edde_api.py`
- `hyperflow/engine/runtime_kernel.py`
- `hyperflow/output/edde_contract.py`
- `hyperflow/output/run_payload.py`
- the storage and checkpoint policy used by the runtime shell

Deferred donor/product API surface:
- `/v1/agents`
- `/v1/workflows`

Everything in `experimental/` and `archive/` is explicitly outside the MVP support contract.

## 7) Shared validation path
Use the shared repo entrypoints instead of ad hoc validation commands:
- `make baseline-qualify`
- `make test`
- `make packaging-smoke`
- `make release-verify`
- `make check`

## 8) Baseline qualification gate
Canonical behavior qualifies only through `make baseline-qualify` / `scripts/baseline_qualification.sh`.
Framework, agent-runtime, platform, and worker metadata may not redefine baseline behavior outside that gate.
