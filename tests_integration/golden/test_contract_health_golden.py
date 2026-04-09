from __future__ import annotations

from hyperflow.contracts.version_policy import CONTRACT_VERSION
from hyperflow.release.contract_golden import load_contract_golden


def test_packaged_contract_health_golden_is_available() -> None:
    golden = load_contract_golden()
    assert golden['schema'] == 'hyperflow/edde-contract/v1'
    assert golden['contract_version'] == CONTRACT_VERSION
    assert golden['input']['emoji_run'] == '🌈💎🔥🧠🔀⚡'
    assert golden['runtime']['pipeline_path'][:2] == ['scan', 'extract']
    assert 'remix' in golden['runtime']['pipeline_path']


def test_golden_contract_preserves_canonical_parser_order() -> None:
    golden = load_contract_golden()
    assert golden['parser']['resolved_edde_phase'] == ['scan', 'extract', 'build', 'reason', 'remix', 'deliver']
    assert golden['parser']['resolution_policy'] == 'longest_match_first'
