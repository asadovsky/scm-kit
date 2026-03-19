#!/usr/bin/env python3

import argparse
import shutil
import sys
from pathlib import Path

from scm_kit.common import PRETTIER_EXTS, PRETTIER_GLOB, check_for_required_tools, get_files_by_ext, has_files, try_run


def lint_code(all_files: bool) -> list[str]:
    """Run all applicable linters. Returns list of failed tool names."""
    failures: list[str] = []

    if (Path.cwd() / "go.mod").exists() and shutil.which("go"):
        if not try_run(["go", "vet", "./..."]):
            failures.append("go vet")

    if has_files(*PRETTIER_EXTS):
        if not try_run(["npx", "prettier", "--check", PRETTIER_GLOB]):
            failures.append("prettier")

    if (Path.cwd() / "biome.json").exists():
        if not try_run(["npx", "@biomejs/biome", "check", "."]):
            failures.append("biome")

    if has_files("py"):
        if not try_run(["uvx", "ruff", "check", "."]):
            failures.append("ruff check")
        if not try_run(["uvx", "ruff", "format", "--check", "."]):
            failures.append("ruff format")

    # Pyright is slow, so we only check changed files by default (use -a for all).
    py_files = list(get_files_by_ext("py", all_files))
    if py_files:
        if not try_run(["uvx", "pyright"] + py_files):
            failures.append("pyright")

    if (Path.cwd() / "tsconfig.json").exists():
        if not try_run(["npx", "tsc", "--noEmit"]):
            failures.append("tsc")

    return failures


def main() -> None:
    check_for_required_tools()
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all-files", action="store_true")
    args = parser.parse_args()
    failures = lint_code(args.all_files)
    if failures:
        print(f"\nLinting failed: {', '.join(failures)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
