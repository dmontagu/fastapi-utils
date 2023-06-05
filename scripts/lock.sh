#!/usr/bin/env bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
cd "${PROJECT_ROOT}"

set -x
poetry lock
poetry export --with dev -f requirements.txt >requirements_tmp.txt
mv requirements_tmp.txt requirements.txt
