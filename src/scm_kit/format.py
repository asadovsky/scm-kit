#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

from scm_kit.common import PRETTIER_EXTS, PRETTIER_GLOB, check_for_required_tools, has_files, maybe_run, run


def format_code() -> None:
    if (Path.cwd() / "go.mod").exists():
        maybe_run(["gofmt", "-s", "-w", "."])
    if has_files(*PRETTIER_EXTS):
        run(["npx", "prettier", "--write", PRETTIER_GLOB])
    if (Path.cwd() / "biome.json").exists():
        run(["npx", "@biomejs/biome", "check", "--write", "."])
    if has_files("py"):
        run(["uvx", "ruff", "check", "--fix-only", "."])
        run(["uvx", "ruff", "format", "."])


def main() -> None:
    check_for_required_tools()
    try:
        format_code()
    except subprocess.CalledProcessError:
        sys.exit(1)


if __name__ == "__main__":
    main()
