# scm-kit

Polyglot formatting and linting toolkit. Provides two commands — `scm-format`
and `scm-lint` — that auto-detect which tools to run based on the files in your
repo.

## Prerequisites

- [Node.js](https://nodejs.org/) (`npx`)
- [uv](https://docs.astral.sh/uv/) (`uvx`)

## Usage

```sh
# Install and run via uvx:
uvx --from scm-kit scm-format
uvx --from scm-kit scm-lint
uvx --from scm-kit scm-lint -a  # lint all files, not just changed

# Or add to your Makefile:
# fmt:
# 	@uvx --from scm-kit scm-format
# lint:
# 	@uvx --from scm-kit scm-lint
```

## What runs

| Language/Files                | Format              | Lint                                 |
| ----------------------------- | ------------------- | ------------------------------------ |
| Go (`go.mod`)                 | `gofmt`             | `go vet`                             |
| JS/TS/CSS/JSON (`biome.json`) | Biome               | Biome                                |
| HTML, Markdown, YAML          | Prettier            | Prettier                             |
| Python (`.py`)                | Ruff (fix + format) | Ruff (check + format check), Pyright |
| TypeScript (`tsconfig.json`)  | —                   | `tsc --noEmit`                       |

Tools are invoked via `npx` or `uvx`, so they don't need to be pre-installed.
Go tools are optional — skipped if not on PATH.

Each tool is skipped when no matching files or config is present, so a
Python-only repo won't invoke Biome or Prettier.

## Config files

Projects using scm-kit should include their own config files as needed:

- `.ruff.toml` — Ruff linter config (Python)
- `biome.json` — Biome formatter/linter config (JS/TS/CSS/JSON)
- `pyrightconfig.json` — Pyright type-checker config (Python)

## Lint flags

- **Default**: Pyright checks only changed files (vs `HEAD` + untracked),
  since it is slow on large codebases. All other linters check the full tree.
- **`-a` / `--all-files`**: Pyright checks all files.

## Development

To test local changes before publishing, use the `dev-` Makefile targets. These
run against the local source instead of the published package:

```sh
make dev-fmt       # format using local scm-kit
make dev-lint      # lint using local scm-kit
make dev-lint-all  # lint all files using local scm-kit
```

## Publishing

```sh
rm -rf dist
uv build
UV_PUBLISH_TOKEN=pypi-xxxxx uv publish
```

Generate a token at https://pypi.org/manage/account/token/.
