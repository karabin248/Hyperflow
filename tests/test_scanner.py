"""
test_scanner.py — Unit tests for the repository scanner module.
"""
import pytest
from scanner.core import (
    compute_overlap_scores,
    analyze_repo_stub,
    detect_language,
    detect_classification,
    extract_dependencies,
)
from pathlib import Path
import tempfile, os


# ── Overlap scoring ────────────────────────────────────────────────────────────

def test_overlap_single_repo_returns_zero():
    repos = [{"id":"r1","name":"hyperflow-core"}]
    scores = compute_overlap_scores(repos)
    assert scores["r1"] == 0.0


def test_overlap_identical_names_returns_high():
    repos = [{"id":"r1","name":"hyperflow-core"},{"id":"r2","name":"hyperflow-core"}]
    scores = compute_overlap_scores(repos)
    assert scores["r1"] == 1.0 and scores["r2"] == 1.0


def test_overlap_disjoint_names_returns_zero():
    repos = [{"id":"r1","name":"alpha"},{"id":"r2","name":"beta"}]
    scores = compute_overlap_scores(repos)
    assert scores["r1"] == 0.0 and scores["r2"] == 0.0


def test_overlap_partial_match():
    repos = [{"id":"r1","name":"hyperflow-core"},{"id":"r2","name":"hyperflow-ui"},{"id":"r3","name":"unrelated"}]
    scores = compute_overlap_scores(repos)
    assert 0 < scores["r1"] < 1.0


# ── Stub analysis ─────────────────────────────────────────────────────────────

def test_stub_api_is_service():
    r = analyze_repo_stub({"id":"x","name":"hyperflow-api","url":""}, 0.5)
    assert r["classification"] == "service"


def test_stub_sdk_is_library():
    r = analyze_repo_stub({"id":"x","name":"hyperflow-sdk","url":""}, 0.0)
    assert r["classification"] == "library"


def test_stub_cli_is_tool():
    r = analyze_repo_stub({"id":"x","name":"hyperflow-cli","url":""}, 0.0)
    assert r["classification"] == "tool"


def test_stub_ts_web_is_typescript():
    r = analyze_repo_stub({"id":"x","name":"hyperflow-ui","url":""}, 0.0)
    assert r["language"] == "typescript"


def test_stub_core_is_python():
    r = analyze_repo_stub({"id":"x","name":"hyperflow-core","url":""}, 0.0)
    assert r["language"] == "python"


def test_stub_includes_all_required_fields():
    r = analyze_repo_stub({"id":"rid","name":"test-repo","url":"http://x"}, 0.1)
    for field in ["id","language","classification","dependencyCount","dependencyNames",
                  "overlapScore","cloneDurationMs","analysisDurationMs","error"]:
        assert field in r


# ── Local tree analysis ────────────────────────────────────────────────────────

def test_detect_language_python():
    with tempfile.TemporaryDirectory() as d:
        for name in ["main.py","utils.py","config.py"]:
            (Path(d)/name).write_text("# python")
        assert detect_language(Path(d)) == "python"


def test_detect_language_typescript():
    with tempfile.TemporaryDirectory() as d:
        for name in ["app.ts","index.ts","server.ts","types.ts"]:
            (Path(d)/name).write_text("// ts")
        assert detect_language(Path(d)) == "typescript"


def test_detect_language_unknown_empty_dir():
    with tempfile.TemporaryDirectory() as d:
        assert detect_language(Path(d)) == "unknown"


def test_detect_classification_service_fastapi():
    with tempfile.TemporaryDirectory() as d:
        (Path(d)/"main.py").write_text("app = fastapi.FastAPI(); uvicorn.run(app)")
        cls, rat = detect_classification(Path(d))
        assert cls == "service"


def test_detect_classification_library_setup_py():
    with tempfile.TemporaryDirectory() as d:
        (Path(d)/"setup.py").write_text("from setuptools import setup; setup(name='mylib')")
        cls, rat = detect_classification(Path(d))
        assert cls == "library"


def test_detect_classification_unknown():
    with tempfile.TemporaryDirectory() as d:
        (Path(d)/"README.md").write_text("# hello")
        cls, rat = detect_classification(Path(d))
        assert cls == "unknown"


def test_extract_dependencies_requirements_txt():
    with tempfile.TemporaryDirectory() as d:
        (Path(d)/"requirements.txt").write_text("fastapi>=0.100\nhttpx>=0.27\npydantic==2.0\n")
        count, names = extract_dependencies(Path(d))
        assert count == 3
        assert "fastapi" in names
        assert "httpx" in names
        assert "pydantic" in names


def test_extract_dependencies_package_json():
    import json
    with tempfile.TemporaryDirectory() as d:
        pkg = {"name":"test","dependencies":{"express":"^5","zod":"^3"}}
        (Path(d)/"package.json").write_text(json.dumps(pkg))
        count, names = extract_dependencies(Path(d))
        assert count == 2
        assert "express" in names


def test_extract_dependencies_empty_dir():
    with tempfile.TemporaryDirectory() as d:
        count, names = extract_dependencies(Path(d))
        assert count == 0 and names == []
