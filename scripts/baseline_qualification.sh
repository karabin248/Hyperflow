#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT_DIR"

export PYTEST_DISABLE_PLUGIN_AUTOLOAD=${PYTEST_DISABLE_PLUGIN_AUTOLOAD:-1}

bash scripts/clean_repo.sh >/dev/null 2>&1 || true
python scripts/import_guard_scan.py

python -m pytest -q       hyperflow/tests/test_baseline_docs_alignment.py       hyperflow/tests/test_runtime_authority_boundaries.py       hyperflow/tests/test_canonical_runtime_path.py       hyperflow/tests/test_command_builder.py       hyperflow/tests/test_emoji_parser.py       hyperflow/tests/test_emoji_action_router.py       hyperflow/tests/test_parser_authority.py       hyperflow/tests/test_emoji_registry.py       hyperflow/tests/test_config_layer.py       hyperflow/tests/test_contract_golden.py       hyperflow/tests/test_run_payload_golden.py       hyperflow/tests/test_run_trace_golden.py       hyperflow/tests/test_edde_contract_schema.py       hyperflow/tests/test_runtime_kernel.py       hyperflow/tests/test_run_payload_serializer.py       hyperflow/tests/test_persistence_failures.py       hyperflow/tests/test_recent_traces.py       hyperflow/tests/test_runtime_persists_trace.py       hyperflow/tests/test_trace_contract_capture.py       hyperflow/tests/test_checkpoint_history.py       hyperflow/tests/test_runtime_storage_policy.py       hyperflow/tests/test_repo_hygiene.py       hyperflow/tests/test_source_zip_real_repo.py       tests/test_run_deterministic_golden.py       tests/test_runtime_guard_negative.py       tests/test_contract_version_lock.py       tests/test_trace_replay.py       tests/test_single_runtime_enforced.py       tests/test_repo_hygiene.py       tests/test_no_unregistered_behavior.py       tests/golden/test_contract_health_golden.py       tests/contracts/test_api_run_contract.py       tests/integration/test_run_creates_checkpoint.py       tests/integration/test_observability_routes.py       tests/integration/test_checkpoint_identity.py       tests/integration/test_worker_metadata.py       tests/integration/test_android_shell_import.py

python -m hyperflow.release_verify --pretty >/dev/null
