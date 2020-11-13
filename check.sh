#!/usr/bin/env sh

set -eux
black --check skam
pylint skam
mypy skam
pytest