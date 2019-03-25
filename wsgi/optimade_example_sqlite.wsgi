#!/usr/bin/env python
#
# Note: see instructions in start_wsgi_example_sqlite.py
#

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from start_wsgi_example_sqlite import app as application
