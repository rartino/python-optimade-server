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
from __future__ import print_function
import cgitb, sys, codecs, cgi

try:
    from urllib.parse import parse_qsl, urlparse
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from urlparse import parse_qsl, urlparse
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class WebError(Exception):
    def __init__(self, message, response_code, response_msg, longmsg=None, content_type='text/plain'):
        super(WebError, self).__init__(message)
        self.content = longmsg if longmsg is not None else message
        self.response_code = response_code
        self.response_msg = response_msg
        self.content_type = content_type


class _CallbackRequestHandler(BaseHTTPRequestHandler):

    get_callbacks = []
    post_callbacks = []
    debug = False

    def get_debug_info(self):
        parsed_path = urlparse(self.path)
        debug_info = {
            'CLIENT': {
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version
            },
            'SERVER': {
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
            }
        }
        return debug_info

    def wfile_write_encoded(self, s):
        self.wfile.write(codecs.encode(s, 'utf-8'))

    def do_GET(self):
        parsed_path = urlparse(self.path)

        relpath = parsed_path.path
        query = dict(parse_qsl(parsed_path.query, keep_blank_values=True))

        if relpath[0] == '/':
            relpath = relpath[1:]

        try:
            for callback in self.get_callbacks:
                output = callback(relpath, query, self.headers)
            self.send_response(output['response_code'])
            self.send_header('Content-type', output['content_type'])
            self.end_headers()
            self.wfile_write_encoded(output['content'])

        except WebError as e:
            self.send_response(e.response_code, e.response_msg)
            self.send_header('Content-type', e.content_type)
            self.end_headers()
            self.wfile_write_encoded(e.content)

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if self.debug:
                self.wfile_write_encoded(cgitb.html(sys.exc_info()))
            else:
                self.wfile_write_encoded("<html><body>An unexpected server error has occured.</body></html>")

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = dict(parse_qsl(self.rfile.read(length), keep_blank_values=True))
        else:
            postvars = {}

        parsed_path = urlparse(self.path)

        relpath = parsed_path.path

        if relpath[0] == '/':
            relpath = relpath[1:]

        try:
            for callback in self.post_callbacks:
                output = callback(relpath, postvars, self.headers)
            self.send_response(output['response_code'])
            self.send_header('Content-type', output['content_type'])
            self.end_headers()
            self.wfile_write_encoded(output['content'])

        except WebError as e:
            self.send_response(e.response_code, e.response_msg)
            self.send_header('Content-type', e.content_type)
            self.end_headers()
            self.wfile_write_encoded(e.content)

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if self.debug:
                self.wfile_write_encoded(cgitb.html(sys.exc_info()))
            else:
                self.wfile_write_encoded("<html><body>An unexpected server error has occured.</body></html>")


def startup(get_callback, post_callback=None, port=80, baseurl=None, debug=False):

    if post_callback is None:
        post_callback = get_callback

    if baseurl is None:
        if port == 80:
            baseurl = "http://localhost/"
        else:
            baseurl = "http://localhost:"+str(port)+"/"

    _CallbackRequestHandler.debug = debug
    _CallbackRequestHandler.get_callbacks += [get_callback]
    _CallbackRequestHandler.post_callbacks += [post_callback]

    server = None
    try:
        server = HTTPServer(('', port), _CallbackRequestHandler)
        print('Started httk webserver on port:', port)
        server.serve_forever()

    except KeyboardInterrupt:
        print('Received keyboard interrupt, shutting down the httk web server')

    finally:
        if server is not None:
            server.socket.close()
            print('Server shutdown complete.')

