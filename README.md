# NRK Subs without the video

## What, why?
Say you're learning Norwegian, and you'd like to pick up some vocabulary or patterns by
watching TV, but they just speak so fast and the subs just fly by and you feel like you're
not picking up as much as you could. If only there was a way to study the subs before
and/or after the episode! That's what this is, a simple app for grabbing the online subs
from NRK and making them easily browsable and, importantly, printable.

## How?
Scraping, mostly.

## Installation
If you just want to run it, use docker to run the flask app.
```bash
$ docker build . -t brbcoffee/subs -f docker/flask/Dockerfile
$ docker run --rm -p 8080:6000 brbcoffee/subs
```
Then point your browser to [http://localhost:8080](http://localhost:8080)

## Development
Install the venv and all packages at the same time with pipenv
```bash
$ pip install pipenv # If you don't already have pipenv installed
$ pipenv install --dev
```