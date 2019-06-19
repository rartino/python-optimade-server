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
This program accepts an URL, or uses http://localhost:8080 if none is given.

It runs code to validate the OPTIMaDe API on that URL.
'''
from __future__ import print_function

import os, sys, argparse
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'src'))

import validation

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Validate OPTiMaDe endpoint at url')

    parser.add_argument('--backend', default=None)
    parser.add_argument('url', nargs='?', default='http://localhost:8080')    
    parser.add_argument('tests', nargs='*', default=[])

    args = parser.parse_args()

    if len(args.tests) > 0:
        tests = args.tests
    else:
        tests = None

    result = validation.run(args.url, tests, backend=args.backend)
    print("==== Validation results of:",args.url)
    pprint(result)
    
    
