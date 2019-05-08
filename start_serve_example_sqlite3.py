#!/usr/bin/env python
#
# Copyright 2019 Rickard Armiento
#
# This file is part of a Python candidate reference implementation of
# the optimade API [https://www.optimade.org/]
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
'''
This is part of a Python candidate reference implementation of the
optimade API [https://www.optimade.org/]. 

This program serves the OPTIMaDe api on http://localhost:8080/
using a test in-memory sqlite3 database setup in the example_sqlite3
backend under src/example_sqlite3. 

Implementations that want to start off from this one, should:

- Copy that backend module into something else, e.g. `example_mydatabase`.

- Edit that backend to serve your own data.

- Copy this program and change it to use that backend instead.
'''
from __future__ import print_function
import os, sys, json, signal
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'src'))
import webserver
import optimade
from parse import parse_optimade_filter, ParserSyntaxError

def handler(signum, frame):
    print('Shutting down on signal',signum)
    exit(0)

signal.signal(signal.SIGINT, handler)
    
def _json_format(response):
    return json.dumps(response, indent=4, separators=(',', ': '), sort_keys=True)

def request_callback(request):

    webserver.check_jsonapi_header_requirements(request['headers'])
    
    try:
        response = optimade.process(request, backend.execute_query, debug = True)
    except optimade.OptimadeError as e:
        raise webserver.JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
    
    return {'content': _json_format(response), 'content_type':'application/vnd.api+json', 'response_code':200, 'response_msg':'OK', 'encoding':'utf-8'}


if __name__ == "__main__":
    
    import backends.example_sqlite3 as backend    
    
    backend.initialize()
    netloc = 'http://localhost:8080'
    basepath = '/'
    webserver.startup(request_callback, port=8080, netloc=netloc, basepath=basepath, debug=True)
    backend.close()


    
