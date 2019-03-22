#!/usr/bin/env python
from __future__ import print_function
import sys, os
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'src'))
from parse import initialize_optimade_parser, parser

ls = initialize_optimade_parser(spaces_hack=True)

demo_string = 'filter=NOT a > b OR c = 100 AND f = "C2 H6"'

filter_ast = parser(ls, demo_string)

pprint(filter_ast)

assert(filter_ast == ('Filter', ('Keyword', ('filter=', 'filter=')), ('Expression', ('Term', ('Atom', ('NOT', 'NOT'), ('Comparison', ('Value', ('Identifier', 'a')), ('Operator', '>'), ('Value', ('Identifier', 'b'))))), ('OR', 'OR'), ('Expression', ('Term', ('Atom', ('Comparison', ('Value', ('Identifier', 'c')), ('Operator', '='), ('Value', ('Number', '100')))), ('AND', 'AND'), ('Term', ('Atom', ('Comparison', ('Value', ('Identifier', 'f')), ('Operator', '='), ('Value', ('String', '"C2 H6"'))))))))))

demo_string = 'filter=_exmpl_melting_point<300 AND nelements=4 AND elements="Si,O2"'

filter_ast = parser(ls, demo_string)
pprint(filter_ast)

assert(filter_ast == ('Filter', ('Keyword', ('filter=', 'filter=')), ('Expression', ('Term', ('Atom', ('Comparison', ('Value', ('Identifier', '_exmpl_melting_point')), ('Operator', '<'), ('Value', ('Number', '300')))), ('AND', 'AND'), ('Term', ('Atom', ('Comparison', ('Value', ('Identifier', 'nelements')), ('Operator', '='), ('Value', ('Number', '4')))), ('AND', 'AND'), ('Term', ('Atom', ('Comparison', ('Value', ('Identifier', 'elements')), ('Operator', '='), ('Value', ('String', '"Si,O2"'))))))))))
