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


from .response import *
from .base_info import *
from .entry import *
from .headers import *
from .schema import schema_validate_request

all_tests = [
    {'name':'base_info_schema', 'relurl':'/structures', 'test':schema_validate_request, 'validation':None},    
    {'name':'base_info', 'relurl':'/info', 'test':validate_base_info_request, 'validation':validate_base_info},

    {'name':'headers', 'relurl':'/info', 'test':validate_headers, 'validation':None},    
    
    {'name':'structures', 'relurl':'/all', 'test':validate_response_request, 'validation':validate_response},
    {'name':'structures', 'relurl':'/structures', 'test':validate_response_request, 'validation':validate_response},
    {'name':'structures_info', 'relurl':'/structures/info', 'test':validate_response_request, 'validation':validate_response},
    {'name':'calculations', 'relurl':'/calculations', 'test':validate_response_request, 'validation':validate_response},
    {'name':'calculations_info', 'relurl':'/calculations/info', 'test':validate_response_request, 'validation':validate_response},

    {'name':'structures_single_entry', 'relurl':'/structures', 'test':validate_single_entry_request, 'validation':validate_response},
    {'name':'calculations_single_entry', 'relurl':'/calculations', 'test':validate_single_entry_request, 'validation':validate_response},
    
]

def run(base_url, tests = None):
    
    results = {}
    
    for test in all_tests:
        if tests == None or test['name'] in tests:
            results[test['name']] = test['test'](base_url, test['relurl'])
        
    return results


