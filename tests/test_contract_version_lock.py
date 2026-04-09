from __future__ import annotations

import pytest

from hyperflow.contracts.version_policy import CONTRACT_VERSION, assert_contract_version
from hyperflow.engine.execution_bundle import ExecutionBundle
from hyperflow.runtime_kernel import run
from hyperflow.language.command_builder import build_command
from hyperflow.schemas.edde_contract_schema import validate_edde_contract
from hyperflow.schemas.errors import SchemaValidationError


def test_execution_bundle_contract_version_is_locked() -> None:
    bundle = ExecutionBundle(
        summary='ok',
        confidence=1.0,
        observer_status='OK',
        next_step='continue',
        execution_path='workflow_step',
    )
    assert bundle.contract_version == CONTRACT_VERSION
    assert_contract_version(bundle.contract_version)


def test_runtime_contract_version_is_emitted_across_output_and_contract() -> None:
    result = run(build_command('🌈💎🔥🧠🔀⚡ prepare a rollout plan'))
    assert result.contract_version == CONTRACT_VERSION
    assert result.to_dict()['contract_version'] == CONTRACT_VERSION
    assert result.edde_contract['contract_version'] == CONTRACT_VERSION


def test_contract_version_drift_requires_explicit_bump() -> None:
    result = run(build_command('🌈💎🔥🧠🔀⚡ prepare a rollout plan'))
    drifted = dict(result.edde_contract)
    drifted['contract_version'] = '1.0.1'
    with pytest.raises(SchemaValidationError, match='Contract version drift detected'):
        validate_edde_contract(drifted)
