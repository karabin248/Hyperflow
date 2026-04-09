import asyncio
import pytest
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run
from hyperflow.output.run_payload import serialize_run_payload

PROMPT_MATRIX = [
    "🧠🔥🌈 analyze global architecture",
    "💎 plan the migration strategy",
    "🔥🔀 build the execution pipeline",
    "analyze the codebase structure",
    "generate a function that adds two numbers",
]


def test_prompt_matrix_builds_commands_and_contracts(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    for prompt in PROMPT_MATRIX:
        cmd = build_command(prompt)
        result = asyncio.run(run(cmd))
        assert result.run_id, f"Missing run_id for prompt: {prompt!r}"
        assert result.summary, f"Missing summary for prompt: {prompt!r}"
        contract = result.edde_contract
        assert contract["schema"] == "hyperflow/edde-contract/v1", (
            f"Bad contract schema for prompt: {prompt!r}"
        )
