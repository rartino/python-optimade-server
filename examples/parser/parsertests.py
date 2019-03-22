#!/usr/bin/env python
from __future__ import print_function
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'src'))
from parse.miniparser import *

print("==========================================")
print("TEST 1: grammar given on bnf ast format")
print("==========================================")

ls_simple_bnf = {
    'start':'S',
    'ignore': ' \t\n',
    'literals': ['+'],
    'tokens': {'id': '[a-zA-Z][a-zA-Z0-9_]*'},
    'bnf_grammar_ast':
    (
     ('S', ('E',)),
     ('E', ('T', '+', 'E')),
     ('E', ('T',)),
     ('T', ('id',)),
    )
}

simple_example = '''
ID + ID
'''

build_ls(ls=ls_simple_bnf)

print("== RULE TABLE")
pprint.pprint(ls_simple_bnf['rule_table'])
print("=============")

print("== ACTION TABLE")
pprint.pprint(ls_simple_bnf['parse_table']['action'])
print("=============")

print("== GOTO TABLE")
pprint.pprint(ls_simple_bnf['parse_table']['goto'])
print("=============")

result = parser(ls_simple_bnf, simple_example)

pprint.pprint(result)

assert(result == ('S', ('E', ('T', ('id', 'ID')), ('+', '+'), ('E', ('T', ('id', 'ID'))))))

print("==========================================")
print("TEST 2: grammar given on ebnf ast format")
print("==========================================")

ls_simple_ebnf = {
    'start':'S',
    'ignore': ' \t\n',
    'literals': ['+'],
    'tokens': {'id': '[a-zA-Z][a-zA-Z0-9_]*'},
    'ebnf_grammar_ast':
    ('Grammar',
     ('Rule',
      ('identifier', 'S'), ('identifier', 'E')
     ),
     ('Rule',
      ('identifier', 'E'),
      ('Concatenation', ('identifier','T'), ('terminal', "'+'"), ('identifier', 'E'))
     ),
     ('Rule',
      ('identifier', 'E'), ('identifier', 'T')
     ),
     ('Rule',
      ('identifier', 'T'), ('identifier', 'id')
     ),
    )
}

build_ls(ls=ls_simple_ebnf)

print("== RULE TABLE")
pprint.pprint(ls_simple_ebnf['rule_table'])
print("=============")

print("== ACTION TABLE")
pprint.pprint(ls_simple_bnf['parse_table']['action'])
print("=============")

print("== GOTO TABLE")
pprint.pprint(ls_simple_bnf['parse_table']['goto'])
print("=============")

simple_example = '''
ID + ID
'''

#result = parser(ls_simple_ebnf, simple_example)

pprint.pprint(result)
assert(result == ('S', ('E', ('T', ('id', 'ID')), ('+', '+'), ('E', ('T', ('id', 'ID'))))))

print("==========================================")
print("TEST 3: Grammar given on ebnf text format")
print("==========================================")

ls_simple_ebnf = {
    'start':'S',
    'ignore': ' \t\n',
    'literals': ['+'],
    'precedence': [],
    'tokens': {'id': '[a-zA-Z][a-zA-Z0-9_]*'},
    'simplify': [],
    'aggregate': [],
    'skip': [],
    'ebnf_grammar':"""
       S = E ;
       E = T, '+', E ;
       E = T ;
       T = id ;
    """
}

build_ls(ls=ls_simple_ebnf)

print("== RULE TABLE")
pprint.pprint(ls_simple_ebnf['rule_table'])
print("=============")

print("== ACTION TABLE")
pprint.pprint(ls_simple_bnf['parse_table']['action'])
print("=============")

print("== GOTO TABLE")
pprint.pprint(ls_simple_bnf['parse_table']['goto'])
print("=============")

simple_example = """
ID + ID
"""

result = parser(ls_simple_ebnf, simple_example)

pprint.pprint(result)
assert(result == ('S', ('E', ('T', ('id', 'ID')), ('+', '+'), ('E', ('T', ('id', 'ID'))))))

print("=====================================================")
print("TEST 4: Parse ebnf grammar using builtin ebnf grammar")
print("=====================================================")

test = """
       S = E ;
       E = T, '+', E ;
       E = E, T ;
       T = id ;
"""

result = parser(ls_ebnf, test)

pprint.pprint(result)    

expect = ('Grammar',
          ('Rule', ('identifier', 'S'), ('identifier', 'E')),
          ('Rule',
           ('identifier', 'E'),
           ('Concatenation',
            ('identifier', 'T'),
            ('terminal', "'+'"),
            ('identifier', 'E'))),
          ('Rule',
           ('identifier', 'E'),
           ('Concatenation', ('identifier', 'E'), ('identifier', 'T'))),
          ('Rule', ('identifier', 'T'), ('identifier', 'id')))

assert(result == expect)

print("=====================================================")
print("TEST 5: Comments")
print("=====================================================")

grammar = """     
     (* The grammar starts with a comment *)
     S = E ;
     E = T, '+', E ;
     (* This is a comment *)
     E = T ;
     T =(* This is a comment in the middle of everything *)id ;    
"""
ls = build_ls(ebnf_grammar=grammar, start='S', ignore=' \t\n',
              comment_markers=[('(*','*)'),('#','\n')],
              literals=['+'],
              tokens={'id': '[a-zA-Z][a-zA-Z0-9_]*'}, verbosity=0)

input_string = """
Tes(* This is a comment *)t #Rest of the line is a comment
+ # Commented out
Test
(* This is a
multiline comment *)
"""
result = parser(ls, input_string, verbosity=0)
print(result)
assert(result == ('S', ('E', ('T', ('id', 'Test')), ('+', '+'), ('E', ('T', ('id', 'Test'))))))
