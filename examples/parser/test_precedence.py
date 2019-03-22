#!/usr/bin/env python
from __future__ import print_function
import sys, os
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'src'))
from parse.miniparser import parser, build_ls, ParserSyntaxError

grammar = """
     S = E ;
     E = E , "*" , E ;
     E = E , "/" , E ;    
     E = E , "+" , E ;
     E = E , "-" , E ;
     E = E , "=" , E ;
     E = id ;
     E = int ;
"""

ls_default = build_ls(ebnf_grammar=grammar, start='S', ignore=' \t\n',
              tokens={'id': '[a-zA-Z][a-zA-Z0-9_]*',
                      'int': '[0-9]+'})

ls_left = build_ls(ebnf_grammar=grammar, start='S', ignore=' \t\n',
              tokens={'id': '[a-zA-Z][a-zA-Z0-9_]*',
                      'int': '[0-9]+'},
              precedence=(('nonassoc','='),('left','+','-'),('left','*','/')))

ls_right = build_ls(ebnf_grammar=grammar, start='S', ignore=' \t\n',
              tokens={'id': '[a-zA-Z][a-zA-Z0-9_]*',
                      'int': '[0-9]+'},
              precedence=(('nonassoc','='),('right','+','-'),('left','*','/')))



print("==== without priority")
input_string = "A + B * C"
result = parser(ls_default, input_string)
print(input_string,"=>")
pprint(result)
assert(result == ('S', ('E', ('E', ('id', 'A')), ('+', '+'), ('E', ('E', ('id', 'B')), ('*', '*'), ('E', ('id', 'C'))))))

input_string = "A * B + C"
result = parser(ls_default, input_string)
print(input_string,"=>")
pprint(result)
assert(result == ('S', ('E', ('E', ('id', 'A')), ('*', '*'), ('E', ('E', ('id', 'B')), ('+', '+'), ('E', ('id', 'C'))))))

print("==== with priority")

input_string = "A + B * C"
result = parser(ls_left, input_string)
print(input_string,"=>")
pprint(result)
assert(result == ('S', ('E', ('E', ('id', 'A')), ('+', '+'), ('E', ('E', ('id', 'B')), ('*', '*'), ('E', ('id', 'C'))))))

input_string = "A * B + C"
result = parser(ls_left, input_string)
print(input_string,"=>")
pprint(result)
assert(result == ('S', ('E', ('E', ('E', ('id', 'A')), ('*', '*'), ('E', ('id', 'B'))), ('+', '+'), ('E', ('id', 'C')))))

print("==== left associativity")

input_string = "A + B + C"

result = parser(ls_left, input_string)
print(input_string,"=>")
pprint(result)
assert(result == ('S', ('E', ('E', ('E', ('id', 'A')), ('+', '+'), ('E', ('id', 'B'))), ('+', '+'), ('E', ('id', 'C')))))

print("==== right associativity")

input_string = "A + B + C"

result = parser(ls_right, input_string)
print(input_string,"=>")
pprint(result)
assert(result == ('S', ('E', ('E', ('id', 'A')), ('+', '+'), ('E', ('E', ('id', 'B')), ('+', '+'), ('E', ('id', 'C'))))))

print("==== non-associativity")

input_string = "A = B = C"
print(input_string,"=>")
try:
    result = parser(ls_right, input_string)
except ParserSyntaxError as e:
    print(e)
    pass
else:
    assert(False)
