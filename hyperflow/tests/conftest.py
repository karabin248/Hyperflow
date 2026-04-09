from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import pytest


sys.dont_write_bytecode = True
os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
os.environ.setdefault('HYPERFLOW_TEST_SESSION_START', str(time.time()))


@pytest.fixture(autouse=True)
def _isolate_test_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    existing = os.environ.get("PYTHONPATH", "")
    pythonpath = str(repo_root) if not existing else f"{repo_root}{os.pathsep}{existing}"
    monkeypatch.setenv("PYTHONPATH", pythonpath)
    monkeypatch.chdir(tmp_path)
