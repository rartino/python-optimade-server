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

import json, time

try:
    from urllib2 import urlopen, HTTPError, URLError, Request
except ImportError:
    from urllib.request import urlopen, HTTPError, URLError, Request

class RequestError(Exception):
    def __init__(self, msg, code):
        super(RequestError, self).__init__(msg)
        self.code = code

def request(url,headers=None):
    retry = 5
    lasterr = None
    while retry > 0:
        try:
            if headers is not None:                
                req = Request(url)
                for header in headers:
                    req.add_header(header, headers[header])
            else:
                req = url
            uo = urlopen(req)
            output = json.load(uo)
            headers = uo.info()
            return {'response':output, 'headers':headers, 'code':uo.code}
        except HTTPError as e:
            raise RequestError("Could not fetch resource: "+str(e), e.code)
        except URLError as e:
            lasterr = e
            retry-=1
            time.sleep(1.0)
    raise RequestError("Could not fetch resource: "+str(lasterr),None)

    
