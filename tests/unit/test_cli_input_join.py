from types import SimpleNamespace

from hyperflow.interface import cli


def test_cli_joins_multiword_input_tokens(monkeypatch, capsys) -> None:
    captured: dict[str, str] = {}

    def fake_build_command(raw: str):
        captured["raw"] = raw
        return SimpleNamespace(
            intent="planning",
            mode="fusion",
            output_type="plan",
            intensity="high",
            tokens=["🌈"],
            operations=["analyze"],
        )

    def fake_run(_command):
        return SimpleNamespace(
            to_dict=lambda: {
                "summary": "ok",
                "confidence": "high",
                "observer_status": "OK",
                "next_step": "none",
            }
        )

    monkeypatch.setattr(cli, "build_command", fake_build_command)
    monkeypatch.setattr(cli, "run", fake_run)
    monkeypatch.setattr(
        "sys.argv",
        ["hyperflow", "create", "module", "plan"],
    )

    cli.main()
    capsys.readouterr()

    assert captured["raw"] == "create module plan"

