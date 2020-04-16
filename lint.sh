#!/usr/bin/env bash
# run on localhost before commit

set -o errexit
set -o nounset
set -x  # we want to print commands

# sort import statements automatically
isort

# run linters
flake8

# run mypy (static type checker for Python)
mypy server*

# run tests with coverage in 4 threads
pytest -n=4 --cov=server --cov=server_tests
