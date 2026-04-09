#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT_DIR"

remove_path() {
  local path="$1"
  if [[ -e "$path" ]]; then
    rm -rf "$path"
    echo "removed $path"
  fi
}

echo "== remove transient build/test residue =="
for path in build dist .pytest_cache .ruff_cache .mypy_cache htmlcov hyperflow-source.zip; do
  remove_path "$path"
done

find . -maxdepth 1 -type f -name "hyperflow-v*-source.zip" -print0 | while IFS= read -r -d "" file; do
  rm -f "$file"
  echo "removed ${file#./}"
done

find . -type d \( -name __pycache__ -o -name '*.egg-info' \) ! -path './docs/_build*' -prune -print0 | while IFS= read -r -d '' dir; do
  rm -rf "$dir"
  echo "removed ${dir#./}"
done

find . -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '.coverage' \) ! -path './docs/_build/*' -print0 | while IFS= read -r -d '' file; do
  rm -f "$file"
  echo "removed ${file#./}"
done

if [[ "${1:-}" == "--deep" ]]; then
  echo "== deep cleanup of generated runtime files =="
  for path in output.json graph.mmd graph.txt status_report.json checkpoint_history.json hyperflow-source.zip; do
    remove_path "$path"
  done
  for path in storage/traces.jsonl storage/knowledge_store.jsonl storage/graph_memory.json; do
    remove_path "$path"
  done
  remove_path storage/checkpoints
  mkdir -p storage/checkpoints
  touch storage/.gitkeep
  echo "removed generated storage payloads"
fi
