#!/usr/bin/env python
""" Runner for the nrk subs app """
import uvicorn  # type: ignore

from skam.server.server import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
