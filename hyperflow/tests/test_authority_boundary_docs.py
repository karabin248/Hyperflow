from __future__ import annotations

from pathlib import Path


def _read(path: str) -> str:
    root = Path(__file__).resolve().parents[2]
    return (root / path).read_text(encoding="utf-8")


def _norm(value: str) -> str:
    return " ".join(value.lower().split())


def test_authority_map_demotes_archive_generated_outputs_and_future_layers() -> None:
    text = _norm(_read("docs/architecture/authority_map.md"))
    assert "generated output, not source truth" in text
    assert "archive material as reference-only" in text
    assert "hyperflow/platform/*" in _read("docs/architecture/authority_map.md")
    assert "explicit promotion decision" in text


def test_docs_index_keeps_boundary_rules_visible() -> None:
    text = _norm(_read("docs/README.md"))
    assert "archive material is reference-only" in text
    assert "generated runtime artifacts are outputs, not canonical source truth" in text
    assert "explicit promotion decision" in text
