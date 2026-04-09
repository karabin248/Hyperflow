# Hyperflow

Hyperflow is the **Hyperflow MVP Runtime Baseline**. It is explicitly defined as an **MVP Core**, a **Runtime Shell**, and a **Minimal Orchestration Layer**.

The baseline is deterministic-first, contract-backed, and intentionally narrow:
- one canonical runtime spine
- one canonical cycle
- explicit runtime contracts
- clean repository baseline rules
- no silent scope inflation into platform or product layers

## Baseline identity
At the current stage, Hyperflow is:
- **MVP Core**
- **Runtime Shell**
- **Minimal Orchestration Layer**
- **Reasoning Authority**
- **Control Authority**

It is **not yet**:
- a full agent runtime
- a platform layer
- a finished product

## Canonical cycle
Canonical full combo: `🌈💎🔥🧠🔀⚡`

Meaning:
- `🌈` = perceive
- `💎` = extract essence / core
- `🔥` = set direction
- `🧠` = synthesize
- `🔀` = generate / compare options
- `⚡` = choose

Legacy order may remain readable for backward compatibility, but it is not canonical behavior.

## Canonical runtime spine
- `hyperflow/interface/cli.py`
- `hyperflow/__main__.py`
- `hyperflow/language/*`
- `hyperflow/control/*`
- `hyperflow/engine/*`
- `hyperflow/output/*`
- `hyperflow/memory/*`
- `hyperflow/checkpoint/*`
- `hyperflow/api/edde_api.py`

Canonical runtime path:

`CLI/API entry -> command construction -> runtime kernel execution -> output / persistence`

There is no second canonical parser, second orchestrator, second CLI root, or parallel runtime shell.
No new canonical behavior may emerge outside the baseline qualification gate.

## MVP public API surface
The canonical MVP app exposes:
- `GET /v1/health`
- `POST /v1/run`
- `GET /v1/checkpoints`
- `GET /v1/checkpoints/latest`
- `GET /v1/checkpoints/{checkpoint_id}`
- `GET /v1/logs/recent`

Deferred donor/product surface:
- `DEFERRED metadata surface (removed from canonical API): GET /v1/agents`
- `DEFERRED metadata surface (removed from canonical API): GET /v1/workflows`

## Storage policy
Generated runtime state is output, not source of truth.

- the repo baseline keeps `storage/` clean
- when Hyperflow runs from the repository root, generated state is redirected to `~/.hyperflow/storage` by default
- set `HYPERFLOW_STORAGE_DIR` to override the storage directory explicitly
- set `HYPERFLOW_STATE_HOME` to change the default state home used for repo-root runs

## Canonical references
- `README.md`
- `docs/README.md`
- `docs/architecture/canonical_runtime.md`
- `docs/architecture/canonical_pipeline.md`
- `docs/architecture/canonical_core.md`
- `docs/architecture/definition_of_done.md`
- `docs/architecture/authority_map.md`
- `docs/architecture/merge_decisions.md`
- `docs/contracts/runtime_contract.md`
- `docs/contracts/api_contract.md`
- `core/CANONICAL_RUNTIME_SURFACE.md`
- `core/BASELINE_ACCEPTANCE.md`
- `core/BASELINE_QUALIFICATION_GATE.md`
- `REPOSITORY_GOVERNANCE.md`

## Future layer status
- `hyperflow/framework/*` — extension-support only, not canonical `/v1/run` authority
- `hyperflow/agent_runtime/*` — real next-layer agent runtime, still outside canonical `/v1/run` authority
  - includes delegation, option generation, reporting handoff, fragment-shaped handoff objects, agent-only delegation profiles, workflow presets, and explicit promotion gates above baseline
- `hyperflow/platform/*` — future platform/product support only
- `hyperflow/platform/workers/*` — metadata-only, not an active worker runtime
- `experimental/` and `archive/` — outside the MVP support contract

## Installation
```bash
pip install -e .
```

Optional API surface:
```bash
pip install -e ".[api]"
uvicorn hyperflow.api.edde_api:create_app --factory --reload
```

## Usage
```bash
hyperflow --version
python -m hyperflow --version
python -m hyperflow.interface.cli --version
hyperflow "🌈💎🔥🧠🔀⚡ Task: build a deployment plan" --pretty
python -m hyperflow "🌈💎🔥🧠🔀⚡ Task: build a deployment plan" --pretty
python -m hyperflow.interface.cli "🌈💎🔥🧠🔀⚡ Task: build a deployment plan" --pretty
```

API example:
```bash
curl -X POST http://127.0.0.1:8000/v1/run \
  -H "Content-Type: application/json" \
  -d '{"prompt":"🌈💎🔥🧠🔀⚡ Task: build a deployment plan"}'
```


## Validation commands
```bash
make test
make baseline-qualify

Canonical parser/control, baseline action routing, baseline action execution helpers, MPS, output contract, and trace/checkpoint semantics all qualify only through this gate.
make packaging-smoke
make release-verify
make check
```

`make test` runs the stable regression suite. `make packaging-smoke` remains the isolated packaging validation path used by local repo gates and CI.

## Clean source zip
```bash
python scripts/make_source_zip.py                    # writes hyperflow-v0.2.0-source.zip containing hyperflow-v0.2.0/
python scripts/make_source_zip.py custom-source.zip
```
This creates a release-friendly source archive that excludes generated build/test/runtime debris.

## Android shell
The imported mobile shell lives in `apps/android/` and remains intentionally decoupled from backend auth, workers, and any second runtime path.


Agent-runtime note: `hyperflow/agent_runtime/*` now includes explicit worker time budgets, failure-mode contracts, and delegation profiles tied to MPS-like operating modes while staying outside canonical `/v1/run` authority.


- agent runtime worker contracts now support explicit retry-policy descriptors above baseline only

- `docs/contracts/agent_runtime_trace_summaries.md` — audit-oriented profile-to-task trace summaries for promotion review and runtime inspection
