SHELL := /bin/bash
.DEFAULT_GOAL := help

pkg_src = fastapi_utils
tests_src = tests
docs_src = docs/src
all_src = $(pkg_src) $(tests_src)

mypy_base = mypy --show-error-codes
mypy = $(mypy_base) $(all_src)
test = pytest --cov=fastapi_utils

.PHONY: all  ## Run the most common rules used during development
all: static test

.PHONY: static  ## Perform all static checks (format, lint, mypy)
static: format lint mypy

.PHONY: test  ## Run tests
test:
	$(test)

.PHONY: format  ## Auto-format the source code (isort, autoflake, black)
format:
	black $(all_src)
	black -l 82 $(docs_src)
	ruff --fix $(all_src)

.PHONY: lint
lint:
	ruff $(all_src)
	black --check --diff $(all_src)
	black -l 82 $(docs_src) --check --diff

.PHONY: mypy  ## Run mypy over the application source and tests
mypy:
	$(mypy)

.PHONY: testcov  ## Run tests, generate a coverage report, and open in browser
testcov:
	$(test)
	@echo "building coverage html"
	@coverage html
	@echo "A coverage report was generated at htmlcov/index.html"
	@if [ "$$(uname -s)" = "Darwin" ]; then \
		open htmlcov/index.html; \
	fi

.PHONY: ci  ## Run all CI validation steps without making any changes to code
ci: lint mypy test

.PHONY: clean  ## Remove temporary and cache files/directories
clean:
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name .coverage`
	rm -f `find . -type f -name ".coverage.*"`
	rm -rf `find . -name __pycache__`
	rm -rf `find . -type d -name '*.egg-info' `
	rm -rf `find . -type d -name 'pip-wheel-metadata' `
	rm -rf `find . -type d -name .pytest_cache`
	rm -rf `find . -type d -name .cache`
	rm -rf `find . -type d -name .mypy_cache`
	rm -rf `find . -type d -name .ruff_cache`
	rm -rf `find . -type d -name htmlcov`
	rm -rf `find . -type d -name "*.egg-info"`
	rm -rf `find . -type d -name build`
	rm -rf `find . -type d -name dist`

.PHONY: lock  ## Update the lockfile
lock:
	./scripts/lock.sh

.PHONY: develop  ## Set up the development environment, or reinstall from the lockfile
develop:
	./scripts/develop.sh

.PHONY: version  ## Bump the version in both pyproject.toml and __init__.py (usage: `make version version=minor`)
version: poetryversion
	$(eval NEW_VERS := $(shell cat pyproject.toml | grep "^version = \"*\"" | cut -d'"' -f2))
	@sed -i "" "s/__version__ = .*/__version__ = \"$(NEW_VERS)\"/g" $(pkg_src)/__init__.py

.PHONY: docs-build  ## Generate the docs and update README.md
docs-build:
	python -m mkdocs build
	cp ./docs/index.md ./README.md
	cp ./docs/contributing.md ./CONTRIBUTING.md

.PHONY: docs-build-ci  ## Generate the docs and check README.md is up-to-date
docs-build-ci:
	python -m mkdocs build
	cmp README.md docs/index.md
	cmp CONTRIBUTING.md docs/contributing.md

.PHONY: docs-format  ## Format the python code that is part of the docs
docs-format:
	isort -rc $(docs_src)
	autoflake -r --remove-all-unused-imports --ignore-init-module-imports $(docs_src) -i
	black -l 82 $(docs_src)

.PHONY: docs-live  ## Serve the docs with live reload as you make changes
docs-live:
	mkdocs serve --dev-addr 0.0.0.0:8008

.PHONY: poetryversion
poetryversion:
	poetry version $(version)

.PHONY: help  ## Display this message
help:
	@grep -E \
		'^.PHONY: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ".PHONY: |## "}; {printf "\033[36m%-16s\033[0m %s\n", $$2, $$3}'
