#!/usr/bin/env python
from __future__ import print_function
import sys, os
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'src'))
from parse import parse_optimade_filter

demo_string = 'NOT a > b OR id > 7'

filter_ast = parse_optimade_filter(demo_string)
pprint(filter_ast)
assert(filter_ast == ('OR',
 ('NOT', ('>', ('Identifier', 'a'), ('Identifier', 'b'))),
 ('>', ('Identifier', 'id'), ('Number', '7'))))

