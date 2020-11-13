#!/usr/bin/env sh

set -eux
black --check skam
isort --check --profile black skam
pylint skam
mypy skam
pytest