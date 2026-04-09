# Canonical Runtime Surface

## Active runtime spine
- CLI entry: `hyperflow/interface/cli.py`
- Module entry: `hyperflow/__main__.py`
- Language/control surface: `hyperflow/language/*`
- Control/policy: `hyperflow/control/*`
- Execution: `hyperflow/engine/*`
- Output contracts: `hyperflow/output/*`
- Persistence/observability: `hyperflow/memory/*`
- Checkpoint surface: `hyperflow/checkpoint/*`
- Canonical API entry: `hyperflow/api/edde_api.py`

This surface is the **Runtime Shell**, the **Reasoning Authority**, the **Control Authority**, and the **Minimal Orchestration Layer** for the Hyperflow MVP Core.

No new canonical behavior may emerge outside the baseline qualification gate.

## Canonical document sources
1. `README.md`
2. `REPOSITORY_GOVERNANCE.md`
3. `docs/README.md`
4. `docs/architecture/canonical_runtime.md`
5. `docs/architecture/canonical_core.md`
6. `docs/architecture/definition_of_done.md`
7. `docs/architecture/authority_map.md`
8. `docs/architecture/merge_decisions.md`
9. `docs/contracts/runtime_contract.md`
10. `docs/contracts/api_contract.md`
11. `core/BASELINE_ACCEPTANCE.md`
12. `core/BASELINE_QUALIFICATION_GATE.md`

## Deferred / Future Layer surfaces
- `experimental/` — research only
- `archive/` — reference only

## Merge rule
Merge capabilities into the active spine. Do not introduce a second parser, second orchestrator, second CLI root, or second top-level runtime shell.
