#!/usr/bin/env python
from __future__ import print_function
from pprint import pprint
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'src'))
from parse.miniparser import parser, build_ls, ParserSyntaxError

grammar = """     
     S = E, { '+', E };
     E = id ;    
"""
ls = build_ls(ebnf_grammar=grammar, start='S', ignore=' \t\n',
              literals=['+'],
              tokens={'id': '[a-zA-Z][a-zA-Z0-9_]*'})

input_string = "Test + Test + Test + Test + Test + Test"

result = parser(ls, input_string)
pprint(result)
assert(result == ('S',
 ('E', ('id', 'Test')),
 ('+', '+'),
 ('E', ('id', 'Test')),
 ('+', '+'),
 ('E', ('id', 'Test')),
 ('+', '+'),
 ('E', ('id', 'Test')),
 ('+', '+'),
 ('E', ('id', 'Test')),
 ('+', '+'),
 ('E', ('id', 'Test'))))
