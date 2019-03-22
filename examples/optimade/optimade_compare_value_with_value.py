#!/usr/bin/env python
from __future__ import print_function
import sys, os
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'src'))
from parse import parse_optimade_filter

demo_string = 'filter=NOT a > b OR 5 > 7'

filter_ast = parse_optimade_filter(demo_string)
pprint(filter_ast)
assert(filter_ast == ('OR',
 ('NOT', ('>', ('Identifier', 'a'), ('Identifier', 'b'))),
 ('>', ('Number', '5'), ('Number', '7'))))

