#!/usr/bin/env sh

set -eux
black --check skam
isort --check --profile black skam
pylint skam
mypy skam
pytest
cd frontend && yarn run eslint --ext ts --ext tsx src/