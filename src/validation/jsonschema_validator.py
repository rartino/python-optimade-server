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

import os, json

from jsonschema import validate, ValidationError

from .request import request, RequestError

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "openapi.new.json")) as f:
    openapi_schema = json.load(f)


def jsonschema_fetch_and_validate(base_url, test, init_result = None):

    if init_result is None:
        result = {'error':[], 'warning':[], 'note':[]}
    else:
        result = init_result
        
    try:
        output = request(base_url+test['relurl'])
    except RequestError as e:
        result['error'] += [{'description':str(e)}]
        return result
    
    try:
        #print "OUTPUT",output['response']
        #print "ON",schema
        schema = openapi_schema['paths'][test['relurl']][test['method'].lower()]['responses']['200']['content']['application/json']['schema']
        schema['components'] = openapi_schema['components']
        validate(output['response'], schema)
    except ValidationError as e:
        result['error'] += [{'description':str(e)}]
    except KeyError as e:
        result['error'] += [{'description':'missing schema parts:'+str(e)}]
        
    return result


    

