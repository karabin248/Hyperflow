import json
from pathlib import Path

from hyperflow.memory.knowledge_store import save_knowledge_object
from hyperflow.memory.traces import append_trace, build_trace_record
from hyperflow.language.command_builder import build_command
from hyperflow.engine.runtime_kernel import run
from hyperflow.output.run_payload import serialize_run_payload


def test_knowledge_store_and_trace(tmp_path: Path):
    raw = (
        "🌈💎🔥🧠🔀⚡ "
        "Task: create a Hyperflow MVP build plan "
        "Goal: extract module order "
        "Format: sections + priorities"
    )

    command = build_command(raw)
    result = run(command)

    payload = serialize_run_payload(command, result)
    payload["run_id"] = "test-run-id"

    knowledge_file = tmp_path / "knowledge.jsonl"
    trace_file = tmp_path / "traces.jsonl"

    save_knowledge_object(payload, knowledge_file)
    trace = build_trace_record("test-run-id", command, result)
    append_trace(trace, trace_file)

    knowledge_lines = knowledge_file.read_text(encoding="utf-8").strip().splitlines()
    trace_lines = trace_file.read_text(encoding="utf-8").strip().splitlines()

    assert len(knowledge_lines) == 1
    assert len(trace_lines) == 1

    loaded_payload = json.loads(knowledge_lines[0])
    loaded_trace = json.loads(trace_lines[0])

    assert loaded_payload["command"]["intent"] == "planning"
    assert loaded_trace["intent"] == "planning"


def test_runtime_persists_top_level_contract_in_knowledge_store():
    raw = (
        "🌈💎🔥🧠🔀⚡ "
        "Task: create a Hyperflow MVP build plan "
        "Goal: extract module order "
        "Format: sections + priorities"
    )

    command = build_command(raw)
    result = run(command)

    knowledge_file = Path("storage/knowledge_store.jsonl")
    knowledge_lines = knowledge_file.read_text(encoding="utf-8").strip().splitlines()
    assert knowledge_lines

    loaded_payload = json.loads(knowledge_lines[-1])
    assert loaded_payload["run_id"] == result.run_id
    assert loaded_payload["contract"]["schema"] == "hyperflow/edde-contract/v1"
    assert loaded_payload["contract"] == result.edde_contract
