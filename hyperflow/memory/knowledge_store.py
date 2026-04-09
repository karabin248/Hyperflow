import json
from pathlib import Path
from typing import Any

from hyperflow.runtime_paths import get_knowledge_file


def save_knowledge_object(payload: dict[str, Any], file_path: Path | None = None) -> Path:
    target = file_path or get_knowledge_file()
    target.parent.mkdir(parents=True, exist_ok=True)

    with target.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    return target
