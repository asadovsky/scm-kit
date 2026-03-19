SHELL := /bin/bash -euo pipefail

.DELETE_ON_ERROR:

########################################
# Format and lint

.PHONY: fmt
fmt:
	@uvx --from scm-kit scm-format

.PHONY: lint
lint:
	@uvx --from scm-kit scm-lint

.PHONY: lint-all
lint-all:
	@uvx --from scm-kit scm-lint -a

########################################
# Dev (use local repo instead of published package)

.PHONY: dev-fmt
dev-fmt:
	@uv run scm-format

.PHONY: dev-lint
dev-lint:
	@uv run scm-lint

.PHONY: dev-lint-all
dev-lint-all:
	@uv run scm-lint -a
