#!/usr/bin/env sh

set -eux
black --check subtitles &
blackpid=$!

isort --check --profile black subtitles &
isortpid=$!

pylint subtitles &
pylintpid=$!

mypy subtitles &
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