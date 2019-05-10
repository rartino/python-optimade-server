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
from .request import request, RequestError

def validate_headers(base_url, relurl='/info'):
    result = {'error':[], 'warning':[], 'note':[]}

    try:
        output = request(base_url+relurl)
    except RequestError as e:
        result['error'] += [{'description':'Unexpected server error:'+str(e)}]
        return
        
    if 'Content-Type' not in output['headers']:
        result['error'] += [{'description':'Server response is missing header Content-Type'}]
    else:
        content_type = output['headers']['Content-Type']
        if content_type != 'application/vnd.api+json':
            result['error'] += [{'description':'Server response Content-Type header is not "application/vnd.api+json"'}]

    try:
        output = request(base_url+relurl,{'Accept':'Content-Type: application/vnd.api+json; unknown_media_type_parameter'})
        if output['code'] != 406:
            result['error'] += [{'description':'Server did not return 406 Not Acceptable for json api 1.0 violating Accept header'}]
    except RequestError as e:
        if e.code != 406:            
            result['error'] += [{'description':'Server did not return 406 Not Acceptable for json api 1.0 violating Accept header'}]
    
    return result
    


