from __future__ import annotations

from pathlib import Path


def _read(path: str) -> str:
    root = Path(__file__).resolve().parents[2]
    return (root / path).read_text(encoding="utf-8")


def _norm(value: str) -> str:
    return " ".join(value.lower().split())


def test_framework_package_is_explicitly_non_canonical() -> None:
    text = _norm(_read("hyperflow/framework/__init__.py"))
    assert "future-layer framework package" in text
    assert "not canonical mvp runtime authority" in text
    assert "explicit promotion decision" in text


def test_platform_package_is_explicitly_non_canonical() -> None:
    text = _norm(_read("hyperflow/platform/__init__.py"))
    assert "future-layer platform package" in text
    assert "not canonical mvp runtime or public api authority" in text
    assert "explicit promotion decision" in text
