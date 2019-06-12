#!/usr/bin/env python
from __future__ import print_function
import sys, os
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'src'))
from parse import initialize_optimade_parser, parser

ls = initialize_optimade_parser()

demo_string = 'NOT a > b OR c = 100 AND f = "C2 H6"'

filter_ast = parser(ls, demo_string)

pprint(filter_ast)

assert(filter_ast == ('Filter', ('Expression', ('ExpressionClause', ('ExpressionPhrase', ('NOT', 'NOT'), ('Comparison', ('IdentifierFirstComparison', ('Identifier', 'a'), ('ValueOpRhs', ('Operator', '>'), ('Value', ('Identifier', 'b'))))))), ('OR', 'OR'), ('Expression', ('ExpressionClause', ('ExpressionPhrase', ('Comparison', ('IdentifierFirstComparison', ('Identifier', 'c'), ('ValueOpRhs', ('Operator', '='), ('Value', ('Number', '100')))))), ('AND', 'AND'), ('ExpressionClause', ('ExpressionPhrase', ('Comparison', ('IdentifierFirstComparison', ('Identifier', 'f'), ('ValueOpRhs', ('Operator', '='), ('Value', ('String', '"C2 H6"'))))))))))))

demo_string = '_exmpl_melting_point<300 AND nelements=4 AND elements="Si,O2"'

filter_ast = parser(ls, demo_string)
pprint(filter_ast)

assert(filter_ast == ('Filter', ('Expression', ('ExpressionClause', ('ExpressionPhrase', ('Comparison', ('IdentifierFirstComparison', ('Identifier', '_exmpl_melting_point'), ('ValueOpRhs', ('Operator', '<'), ('Value', ('Number', '300')))))), ('AND', 'AND'), ('ExpressionClause', ('ExpressionPhrase', ('Comparison', ('IdentifierFirstComparison', ('Identifier', 'nelements'), ('ValueOpRhs', ('Operator', '='), ('Value', ('Number', '4')))))), ('AND', 'AND'), ('ExpressionClause', ('ExpressionPhrase', ('Comparison', ('IdentifierFirstComparison', ('Identifier', 'elements'), ('ValueOpRhs', ('Operator', '='), ('Value', ('String', '"Si,O2"'))))))))))))

