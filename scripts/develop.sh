#!/usr/bin/env bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
cd "${PROJECT_ROOT}"

check_for_python3() {
  command -v python3 >/dev/null 2>&1 || {
    cat <<ERROR >&2
***Required*** command not found: python3

If pyenv is installed, you can install python3 via:

    pyenv install 3.8.1  # update version as desired

See the following links for more information:
* https://github.com/pyenv/pyenv
* https://github.com/pyenv/pyenv-installer

ERROR
    exit 1
  }
}

check_for_poetry() {
  command -v poetry >/dev/null 2>&1 || {
    cat <<ERROR >&2
***Required*** command not found: poetry

This can be installed via:

    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3

See the following links for more information:
* https://poetry.eustace.io/docs/
* https://github.com/sdispater/poetry

ERROR
    exit 1
  }
}

check_for_python3
check_for_poetry

set -x
poetry run pip install -r requirements.txt
poetry install

{ set +x; } 2>/dev/null
echo ""
echo "Virtual environment interpreter installed at:"
poetry run python -c "import sys; print(sys.executable)"
