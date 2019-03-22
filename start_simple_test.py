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

This program runs a simple test query against the example_sqlite3 backend.
'''
from __future__ import print_function
import os, sys
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'src'))
from parse import parse_optimade_filter

if __name__ == "__main__":

    import example_sqlite3 as backend    
    
    backend.initialize()

    # This represents the query being received (later to be received via a web URL query)
    tables = ["structures"]
    response_fields = ["id", "chemical_formula", "elements"]

    if len(sys.argv) >= 2:
        input_string = 'filter='+sys.argv[1]
    else:
        input_string = 'filter=elements="Ga,Ti" AND (nelements=3 OR nelements=2)'
        
    response_limit = 50
    
    filter_ast = parse_optimade_filter(input_string)

    print("==== FILTER STRING PARSE RESULT:")
    pprint(filter_ast)
    print("====")

    result = backend.execute_query(tables, response_fields, response_limit, filter_ast, debug=True)

    print("==== END RESULT")
    pprint(list(result))
    print("===============")
    
    backend.close()

