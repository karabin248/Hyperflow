from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from typing import Any

from hyperflow.release.contract_golden import (
    load_contract_golden,
    normalize_contract_for_golden,
)

CANONICAL_HEALTH_CHECK = "🌈💎🔥🧠🔀⚡ runtime contract health check"


@dataclass
class CommandCheck:
    name: str
    argv: list[str]
    stdout: str


def _run_cli(*args: str) -> CommandCheck:
    argv = [sys.executable, "-m", "hyperflow", *args]
    completed = subprocess.run(argv, check=True, capture_output=True, text=True)
    return CommandCheck(name=" ".join(args), argv=argv, stdout=completed.stdout.strip())


def build_release_verification() -> dict[str, Any]:
    version = _run_cli("--version")
    payload_check = _run_cli(CANONICAL_HEALTH_CHECK)
    status = _run_cli("--status-report")
    recent = _run_cli("--recent", "--recent-limit", "1")
    checkpoint_history = _run_cli("--checkpoint-history", "--checkpoint-history-limit", "1")

    payload_document = json.loads(payload_check.stdout)
    contract_document = payload_document.get("contract", {})
    normalized_contract = normalize_contract_for_golden(contract_document)
    contract_golden = load_contract_golden()

    return {
        "status": "PASS" if normalized_contract == contract_golden else "FAIL",
        "version": version.stdout,
        "checks": {
            "canonical_health_check": {
                "command": payload_check.argv,
                "run_id": payload_document.get("run_id"),
                "intent": payload_document.get("intent"),
                "mode": payload_document.get("mode"),
                "normalized_contract_matches_golden": normalized_contract == contract_golden,
            },
            "status_report": {
                "command": status.argv,
                "stdout": status.stdout,
            },
            "recent_runs": {
                "command": recent.argv,
                "stdout": recent.stdout,
            },
            "checkpoint_history": {
                "command": checkpoint_history.argv,
                "stdout": checkpoint_history.stdout,
            },
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Hyperflow release verification checks.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print verification output")
    args = parser.parse_args(argv)

    verification = build_release_verification()
    output = (
        json.dumps(verification, indent=2, ensure_ascii=False)
        if args.pretty
        else json.dumps(verification, ensure_ascii=False)
    )
    print(output)
    return 0 if verification["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
