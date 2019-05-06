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

This is a wsgi implementation that serves the OPTIMaDe api on
http://localhost:8080/ using a test in-memory sqlite3 database setup
in the example_sqlite3 backend under src/example_sqlite3.

By executing this file you serve the app using the python built-in wsgi 
server, which is intended for tests.

To serve the app via apache:

- Make sure to have mod-wsgi installed (e.g., `apt install libapache2-mod-wsgi` on Debian/Ubuntu; `yum install mod_wsgi` on RedHat, Fedora, OpenSUSE, etc., and run `a2enmod wsgi`.) 

- Copy the whole app (i.e., all python files, etc.) into /var/www/optimade/

- Setup apache with a VirtualHost looking something like this:

```
Listen 8088
<VirtualHost *:8088>
    ServerName localhost

    WSGIDaemonProcess optimade_example_sqlite processes=4 threads=1
    WSGIScriptAlias / /var/www/optimade/wsgi/optimade_example_sqlite.wsgi

    <Directory /var/www/optimade/wsgi/>
        WSGIProcessGroup optimade_example_sqlite
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>
```
- (Re)start apache2.


Notes: 
- The port is here set to 8088 so that both this and other tests
on 8080 can run at the same time.
- Parallelism is done here over processes instead of threads.
The Python interpreter can only execute on one thread at a time
due to a feature called 'GIL', and it is also very difficult to
know if Python library code is thread-safe or not. Threads can 
still be beneficial in some cases, e.g., when most time is spent
waiting for heavy IO load, but without serious benchmarking it
is safer to do parallelism over processes than threads.)

Implementations that want to start off from this one, should:

- Copy that backend module into something else, e.g. `example_mydatabase`.

- Edit that backend to serve your own data.

- Copy this program and change it to use that backend instead.
'''
from __future__ import print_function
import os, sys, json, codecs
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'src'))
import webserver
import optimade
from parse import parse_optimade_filter, ParserSyntaxError
import backends.example_sqlite3 as backend   

baseurl = None

def _json_format(response):
    return codecs.encode(json.dumps(response, indent=4, separators=(',', ': '), sort_keys=True),'utf-8')

def app(environ, start_response):

    headers = webserver.wsgi_get_headers(environ)
    query = webserver.wsgi_get_query(environ)
    relurl = webserver.wsgi_get_relurl(environ)
    
    webserver.check_jsonapi_header_requirements(headers)
    
    try:
        response = optimade.process(baseurl, relurl, query, backend.execute_query, debug = True)
    except optimade.OptimadeError as e:
        error = webserver.JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        
        start_response(str(error.response_code) + " "+str(error.response_msg), [('Content-Type',error.content_type)])
        return [error.content]

    start_response('200 OK', [('Content-Type','application/vnd.api+json')])
    return [_json_format(response)]


backend.initialize()

if __name__ == "__main__":

    baseurl = 'http://localhost:8080/'
    
    from wsgiref.simple_server import make_server

    srv = make_server('localhost', 8080, app)
    srv.serve_forever()
    backend.close()

    
