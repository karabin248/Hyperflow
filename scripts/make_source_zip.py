#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from hyperflow.release.source_zip import build_source_zip, default_source_zip_name


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a clean source zip for the current repo.")
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Output zip path (default: hyperflow-v<version>-source.zip)",
    )
    args = parser.parse_args()

    root = Path.cwd()
    output = Path(args.output or default_source_zip_name(root))
    build_source_zip(root, output)
    print(output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
