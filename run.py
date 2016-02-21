#!/usr/bin/env python
import sys

from website import app

if __name__ == "__main__":
    if "lan" in sys.argv:
        app.run(host='0.0.0.0')
    else:
        app.run(port=5000)
