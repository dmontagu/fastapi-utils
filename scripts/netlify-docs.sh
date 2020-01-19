#!/usr/bin/env bash
set -x
set -e

# Install pip
cd /tmp
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.6 get-pip.py --user
cd -

# Install poetry to be able to install all
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3.6

make develop
make docs-build
