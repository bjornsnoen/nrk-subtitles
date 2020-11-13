#!/usr/bin/env sh

set -eux
black --check skam
isort --check skam
pylint skam
mypy skam
pytest