# Hyperflow MVP Runtime Baseline — Definition of Done

This document maps the baseline acceptance gate to concrete files, tests, and validation commands in this repository.

## 1. Canon is explicit
- **Files:** `README.md`, `REPOSITORY_GOVERNANCE.md`, `core/CANONICAL_RUNTIME_SURFACE.md`, `core/BASELINE_QUALIFICATION_GATE.md`
- **Locked statement:** Hyperflow is the MVP Core, Runtime Shell, Reasoning Authority, Control Authority, and Minimal Orchestration Layer.
- **Gate rule:** No new canonical behavior may emerge outside the baseline qualification gate.

## 2. One runtime spine exists
- **Files:** `hyperflow/interface/cli.py`, `hyperflow/__main__.py`, `hyperflow/api/edde_api.py`, `hyperflow/engine/runtime_kernel.py`
- **Tests:** `hyperflow/tests/test_cli_entrypoint.py`, `tests/contracts/test_api_run_contract.py`

## 3. Canonical cycle is locked
- **Files:** `README.md`, `core/MVP_RUNTIME_FREEZE.md`, config fixtures under `hyperflow/configs/`
- **Tests:** `hyperflow/tests/test_command_builder.py`, `hyperflow/tests/test_config_layer.py`

## 4. Runtime contracts are stable
- **Files:** `docs/contracts/runtime_contract.md`, `docs/contracts/api_contract.md`, `core/CORE_MODULE_REGISTRY.md`
- **Tests:** `hyperflow/tests/test_contract_golden.py`, `hyperflow/tests/test_run_payload_golden.py`, `hyperflow/tests/test_edde_contract_schema.py`
- **Locked semantic statement:** Parser / control, baseline action routing, baseline action execution helpers, MPS, and output contract authority are test-backed through the baseline qualification gate.

## 5. Core runtime behavior is test-backed
- **Tests:** `hyperflow/tests/test_cli_entrypoint.py`, `hyperflow/tests/test_runtime_kernel.py`, `hyperflow/tests/test_run_payload_serializer.py`, `hyperflow/tests/test_persistence_failures.py`, `tests/integration/test_run_creates_checkpoint.py`

## 6. Core trace / checkpoint authority is test-backed
- **Files:** `hyperflow/memory/traces.py`, `hyperflow/checkpoint/snapshot.py`, `hyperflow/checkpoint/history.py`, `hyperflow/api/routes_logs.py`, `hyperflow/api/routes_checkpoints.py`
- **Tests:** `hyperflow/tests/test_recent_traces.py`, `hyperflow/tests/test_runtime_persists_trace.py`, `hyperflow/tests/test_trace_contract_capture.py`, `hyperflow/tests/test_checkpoint_history.py`, `hyperflow/tests/test_runtime_storage_policy.py`, `tests/integration/test_observability_routes.py`, `tests/integration/test_checkpoint_identity.py`

## 7. Repository baseline is clean
- **Files:** `.gitignore`, `storage/.gitkeep`, `storage/checkpoints/.gitkeep`
- **Tests:** `hyperflow/tests/test_repo_hygiene.py`, `hyperflow/tests/test_source_zip_real_repo.py`

## 8. Docs match runtime truth
- **Files:** `README.md`, `REPOSITORY_GOVERNANCE.md`, `core/CANONICAL_RUNTIME_SURFACE.md`, `docs/architecture/authority_map.md`
- **Tests:** `hyperflow/tests/test_baseline_docs_alignment.py`

## 9. Baseline is self-sufficient
- **Files:** `docs/README.md`, `docs/architecture/canonical_runtime.md`, `core/BASELINE_ACCEPTANCE.md`

## 10. New work mainly hardens, not redefines
- **Files:** `docs/architecture/merge_decisions.md`, `REPOSITORY_GOVERNANCE.md`

## 11. Scope boundaries are enforceable
- **Files:** `REPOSITORY_GOVERNANCE.md`, `core/CANONICAL_RUNTIME_SURFACE.md`, `docs/architecture/authority_map.md`
- **Tests:** `tests/integration/test_worker_metadata.py`, `tests/integration/test_inventory_routes.py`

## 12. Decision logging is durable
- **Files:** `docs/architecture/merge_decisions.md`, `core/BASELINE_ACCEPTANCE.md`

## 13. Future phases become separate by default
- **Files:** `README.md`, `REPOSITORY_GOVERNANCE.md`, `core/CANONICAL_RUNTIME_SURFACE.md`

## Validation command
```bash
make baseline-qualify
```
