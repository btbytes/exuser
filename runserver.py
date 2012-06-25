#!/usr/bin/env python

from os import environ
from exuser import app

app.run('0.0.0.0', 7001, debug=True)
