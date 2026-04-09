#!/usr/bin/env python3
from __future__ import annotations

import ast
from pathlib import Path

DENY = {"hyperflow.framework", "hyperflow.platform", "hyperflow.agent_runtime"}
ROOTS = [Path("hyperflow"), Path("tests")]

violations: list[str] = []
for root in ROOTS:
    if not root.exists():
        continue
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                if any(name == blocked or name.startswith(blocked + ".") for blocked in DENY):
                    violations.append(f"{path}:{getattr(node, 'lineno', 0)}:{name}")
if violations:
    print("\n".join(sorted(violations)))
    raise SystemExit(1)
