import asyncio
import json
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run
from hyperflow.output.run_payload import serialize_run_payload


def test_serialize_run_payload_builds_shared_top_level_envelope(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("🧠🔥 serialize payload test")
    result = asyncio.run(run(cmd))
    payload = serialize_run_payload(cmd, result)
    assert "command" in payload
    assert "result" in payload
    assert payload["result"]["run_id"] == result.run_id
    # Ensure JSON-serializable
    json.dumps(payload)
