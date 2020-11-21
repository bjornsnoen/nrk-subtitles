#!/usr/bin/env python
""" Runner for the nrk subs app """
from os import getenv

import uvicorn  # type: ignore

from subtitles.server.server import app

if getenv("DEBUG") == "1":
    import debugpy  # type: ignore

    host = getenv("DEBUG_LISTEN_HOST")
    port = getenv("DEBUG_LISTEN_PORT")
    if host is not None and port is not None:
        debugpy.listen((host, int(port)))
    else:
        debugpy.listen(5678)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
