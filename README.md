# NRK Subs without the video

## What, why?
Say you're learning Norwegian, and you'd like to pick up some vocabulary or patterns by
watching TV, but they just speak so fast and the subs just fly by and you feel like you're
not picking up as much as you could. If only there was a way to study the subs before
and/or after the episode! That's what this is, a simple app for grabbing the online subs
from NRK and making them easily browsable and, importantly, printable.

## How?
Nowadays we're using NRK's API for everything except finding out what shows they have, for
that part we're just scraping tv.nrk.no with requests and beautifulsoup.

## Installation
If you just want to run it, use docker to run the full stack.
```bash
$ docker build . -t brbcoffee/subs -f docker/fastapi/Dockerfile
$ docker run --rm -p 8080:80 brbcoffee/subs
```
Then point your browser to [http://localhost:8080](http://localhost:8080)

Or with docker-compose (preconfigured for development)
```bash
$ docker-compose up -d
```

## Development
Install the venv and all packages at the same time with pipenv and yarn
```bash
$ pip install pipenv # If you don't already have pipenv installed
$ pipenv install --dev
$ cd frontend
$ yarn install --dev
```

As mentioned, the docker-image is preconfigured for development. Simply up the stack and you can attach to the python api on port 5678 (pydebug). The react frontend will autoreload both the server and in the browser on code changes. This is a working launch configuration for both in vscode:

```json
{
    "configurations": [
        {
            "name": "Frontend debug",
            "type": "pwa-chrome",
            "request": "launch",
            "sourceMapPathOverrides": {
                "/app/*": "${workspaceFolder}/*"
            },
            "runtimeExecutable": "/usr/bin/chromium",
            "url": "http://localhost/show/skam/season/1/episode/2"
        },
        {
            "name": "Docker: Attach to python",
            "type": "python",
            "request": "attach",
            "host": "localhost",
            "port": 5678,
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/app"
                }
            ]
        }
    ]
}
```
Only the `sourceMapPathOverrides` should be of any interest, it's necessary in order to serve the app in docker and get vscode to recognize where the files actually are in the project.