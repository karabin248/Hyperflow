from __future__ import annotations

import json
import sys
from pathlib import Path

import hyperflow.runtime_kernel as runtime_kernel
from hyperflow.interface import cli
from hyperflow.language import command_builder
from hyperflow.schemas import edde_contract_schema


def test_cli_input_flows_through_canonical_runtime_path(monkeypatch, capsys, tmp_path: Path) -> None:
    assert cli.build_command is command_builder.build_command
    assert cli.run is runtime_kernel.run
    assert edde_contract_schema.validate_edde_contract is not None

    contract_checks = {"count": 0}
    original_validate = edde_contract_schema.validate_edde_contract

    def _record_contract_validation(contract: dict) -> None:
        contract_checks["count"] += 1
        original_validate(contract)

    def _framework_not_expected():
        raise AssertionError("framework runtime path must not own plain CLI prompt execution")

    monkeypatch.setattr("hyperflow.engine.runtime_kernel.validate_edde_contract", _record_contract_validation)
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    monkeypatch.setattr(sys, "argv", ["hyperflow", "🌈💎🔥🧠🔀⚡", "canonical runtime path check"])

    cli.main()

    output = capsys.readouterr().out
    payload = json.loads(output)

    assert contract_checks["count"] == 1
    assert payload["contract"]["schema"] == "hyperflow/edde-contract/v1"
    assert payload["contract"]["timeline"][-1]["phase"] == "OUTPUT"
