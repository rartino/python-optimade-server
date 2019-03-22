#!/usr/bin/env python
from __future__ import print_function
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'src'))
from parse.miniparser import parser, build_ls, ParserSyntaxError

grammar = """     
     S = E ;
     E = T, '+', E ;
     E = T ;
     T = id ;    
"""
ls = build_ls(ebnf_grammar=grammar, start='S', ignore=' \t\n',
              literals=['+'],
              tokens={'id': '[a-zA-Z][a-zA-Z0-9_]*'})

input_string = "Test + Test"

result = parser(ls, input_string)
print(result)
assert(result == ('S', ('E', ('T', ('id', 'Test')), ('+', '+'), ('E', ('T', ('id', 'Test'))))))

input_string = "Test + + Test"

try:
  result = parser(ls, input_string)
except ParserSyntaxError as e:
    print(str(e))
    assert(e.info == "unexpected symbol")
    assert(e.line == 1)
    assert(e.pos == 8)
    assert(e.linestr == "Test + + Test")
else:
    assert(False)
    
input_string = "Test + - Test"

try:
  result = parser(ls, input_string)
except ParserSyntaxError as e:
    print(str(e))
    assert(e.info == "unrecognized symbol")
    assert(e.line == 1)
    assert(e.pos == 8)
    assert(e.linestr == "Test + - Test")
else:
    assert(False)
   
grammar = """     
     S = E ;
     E = T, '++', E ;
     E = T ;
     T = id ;    
"""
ls = build_ls(ebnf_grammar=grammar, start='S', ignore=' \t\n',
              literals=['+'],
              tokens={'id': '[a-zA-Z][a-zA-Z0-9_]*', '++':'\+\+'})

input_string = "Test ++ Test"

result = parser(ls, input_string)
print(result)
assert(result == ('S', ('E', ('T', ('id', 'Test')), ('++', '++'), ('E', ('T', ('id', 'Test'))))))


