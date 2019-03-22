#!/usr/bin/env python
from __future__ import print_function
import sys, os
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'src'))
from parse import parse_optimade_filter

demo_string = 'filter=NOT a > b OR c = 100 AND f = "C2 H6"'

filter_ast = parse_optimade_filter(demo_string)
pprint(filter_ast)
assert(filter_ast == ('OR',
 ('NOT', ('>', ('Identifier', 'a'), ('Identifier', 'b'))),
 ('AND',
  ('=', ('Identifier', 'c'), ('Number', '100')),
  ('=', ('Identifier', 'f'), ('String', '"C2 H6"')))))

demo_string = 'filter=_exmpl_melting_point<300 AND nelements=4 AND elements="Si,O2"'

filter_ast = parse_optimade_filter(demo_string)
pprint(filter_ast)
assert(filter_ast == ('AND',
 ('<', ('Identifier', '_exmpl_melting_point'), ('Number', '300')),
 ('AND',
  ('=', ('Identifier', 'nelements'), ('Number', '4')),
  ('=', ('Identifier', 'elements'), ('String', '"Si,O2"')))))
