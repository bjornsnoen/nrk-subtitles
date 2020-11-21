#!/usr/bin/env sh

set -eux
black --check skam &
blackpid=$!

isort --check --profile black skam &
isortpid=$!

pylint skam &
pylintpid=$!

mypy skam &
mypypid=$!

pytest &
pytestpid=$!

cd frontend && yarn run eslint --ext ts --ext tsx src/ &
eslintpid=$!

wait ${blackpid}
wait ${isortpid}
wait ${pylintpid}
wait ${mypypid}
wait ${pytestpid}
wait ${eslintpid}