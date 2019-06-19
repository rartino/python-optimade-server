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

from .single_entry import prepare_single_entry

all_tests = [
    {'name':'base_info', 'relurl':'/structures', "method":'GET'},
    {'name':'base_info', 'relurl':'/info', "method":'GET'},
    {'name':'structures', 'relurl':'/structures', "method":'GET'},
    {'name':'structures_info', 'relurl':'/structures/info', "method":'GET'},
    {'name':'calculations', 'relurl':'/calculations', "method":'GET'},
    {'name':'calculations_info', 'relurl':'/calculations/info', "method":'GET'},

    {'name':'structures_single_entry', 'relurl':'/structures', 'prepare':prepare_single_entry, "method":'GET'},
    {'name':'calculations_single_entry', 'relurl':'/calculations', 'prepare':prepare_single_entry, "method":'GET'},
]

def run(base_url, tests = None, backend=None):

    if backend is None:
        backend = "openapi_core"

    if backend == "jsonschema":
        from .jsonschema_validator import jsonschema_fetch_and_validate as fetch_and_validate
        
    elif backend == "openapi_core":
        from .openapi_core_validator import openapi_core_fetch_and_validate as fetch_and_validate

    elif backend == "adhoc":
        from .adhoc_validator import adhoc_fetch_and_validate as fetch_and_validate

    else:
        raise Ecception("Unknown backend:"+str(backend))
    
        
    results = {}
    
    for test in all_tests:
        if tests is None or test['name'] in tests:
            if 'prepare' in test:
                init_result = test['prepare'](base_url, dict(test))
            else:
                init_result = None
            if 'stop' not in test or not test['stop']:
                results[test["name"]] = fetch_and_validate(base_url, test,init_result=init_result)
                
        
    return results


