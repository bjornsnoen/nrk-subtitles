#!/usr/bin/env python
""" Runner for the nrk subs app """
from skam.server.server import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
