from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import pytest

from hyperflow.engine.reasoning import get_llm_backend, set_llm_backend


sys.dont_write_bytecode = True
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("HYPERFLOW_TEST_SESSION_START", str(time.time()))


class MockLLMBackend:
    def __init__(self, response=("Mock LLM response: analysis complete.", "mock-model-v1"), fail: bool = False):
        self.calls = []
        self._response = response
        self._fail = fail

    async def __call__(self, prompt, intent, mode):
        self.calls.append({"prompt": prompt, "intent": intent, "mode": mode})
        if self._fail:
            raise RuntimeError("Mock LLM failure")
        return self._response


@pytest.fixture(autouse=True)
def _isolate_repo_side_effects(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    existing = os.environ.get("PYTHONPATH", "")
    pythonpath = str(repo_root) if not existing else f"{repo_root}{os.pathsep}{existing}"
    monkeypatch.setenv("PYTHONPATH", pythonpath)
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def mock_llm():
    original = get_llm_backend()
    backend = MockLLMBackend()
    set_llm_backend(backend)
    yield backend
    set_llm_backend(original)


@pytest.fixture
def no_llm():
    original = get_llm_backend()
    set_llm_backend(None)
    yield
    set_llm_backend(original)
