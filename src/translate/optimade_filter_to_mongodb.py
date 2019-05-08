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
This file provides functions to translate an OPTIMaDe filter string into a mongodb query. 
'''

from __future__ import print_function
import re
from pprint import pprint

from .error import TranslatorError

supported_dialects = ['3.6']


def optimade_filter_to_mongodb(dialect, filter_ast, entries, response_fields, collection_mapper, fields_mapper, response_limit):

    if dialect not in supported_dialects:
        raise Exception("optimade_filter_to_mongodb: Requested dialect is not supported: "+str(dialect))

    projection = set(response_fields)
    queries = []

    for entry in entries:
        if filter_ast is not None:
            query = optimade_filter_to_mongodb_recurse(filter_ast, fields_mapper[entry], optimade_valid_fields_per_entry[entry])
        else:
            query = {}            
        queries += [{'query': query, 'collection': collection_mapper[entry], 'type':'find'}]

    return {'queries': queries, 'projection': list(projection), 'limit': response_limit}


_opmap = {'!=': '$ne', '>': '$gt', '<': '$lt', '=': '$eq', '<=': '$lte', '>=': '$gte', 'AND': '$and', 'OR': '$or', 'NOT': '$not'}    


def optimade_filter_to_mongodb_recurse(node, fields_mapper, fields_handlers, recursion=0):

    query = {}
    if node[0] in ['AND', 'OR']:
        query = {
            _opmap[node[0]]: {
                optimade_filter_to_mongodb_recurse(node[1], fields_mapper, fields_handlers, recursion=recursion+1),
                optimade_filter_to_mongodb_recurse(node[1], fields_mapper, fields_handlers, recursion=recursion+1)
            }
        }
    elif node[0] in ['NOT']:
        query = {'$not': optimade_filter_to_mongodb_recurse(node[1], fields_mapper, fields_handlers, recursion=recursion+1)
                 }
    elif node[0] in ['>', '>=', '<', '<=', '=', '!=']:
        op = node[0]
        left = node[1]
        right = node[2]
        if left[0] == 'Value' and right[0] == 'Value':
            # This is apparently allowed in the grammar? **            
            query = unknown_types_handler(op, left[1], right[1])
        else:
            if left[0] == 'Identifier' and right[0] == 'Value':
                left, right = right, left
            assert(left[0] == 'Identifier')
            field = fields_mapper[left[1]] 
            argtype, handler = fields_handlers[left[1]] 
            assert(right[0] == argtype)
            value = right[1]
            query = handler(field, op, value)
    else:
        pprint(node)
        raise TranslatorError("Unexpected translation error", 500, "Internal server error.")
    return query


def string_handler(field, op, value):
    op = _opmap[op]
    value = value[1:-1]
    return {field: {op: value}}


def integer_handler(field, op, value):
    op = _opmap[op]
    value = value[1:-1]
    return {field: {op: value}}


def elements_handler(field, op, value):

    if op != '=':
        raise TranslatorError("Elements can only be compared with equals operator.", 400, "Bad request.")

    segments = []
    value = value[1:-1]
    elements = [x.strip() for x in value.split(",")]
    return {field: {'$all': elements}}

# Assumes the formula is stored according to element name in the database


def chemical_formula_handler(field, op, value):

    if op != '=':
        raise TranslatorError("Chemical formulas can only be compared with equals operator.", 400, "Bad request.")

    value = value[1:-1]
    segments = sorted(re.findall('[A-Z][a-z]?[0-9]*', value))
    sorted_formula = "".join(segments)
    return {field: {'$eq': sorted_formula}}


def formula_prototype_handler(field, op, value):

    if op != '=':
        raise TranslatorError("Formula prototypes can only be compared with equals operator.", 400, "Bad request.")

    value = value[1:-1]
    try:
        segments = sorted((int(x[1]), x[0]) for x in re.findall('([A-Z][a-z]?)([0-9]*)', value))
    except ValueError:
        raise TranslatorError("Misformed formula_prototype request.", 400, "Bad request.")
    sorted_formula = "".join([x[1]+str(x[0]) for x in segments])
    return {field: {'$eq': sorted_formula}}


def unknown_types_handler(val1, op, val2):
    op = _opmap[op]
    return {'$expr': {op: [val1, val2]}}


optimade_valid_fields_per_entry = {
    'structures': {
        'id': ('String', string_handler),
        'modification_date': ('String', string_handler),
        'elements': ('String', elements_handler),
        'nelements': ('Number', integer_handler),
        'chemical_formula': ('String', chemical_formula_handler),
        'formula_prototype': ('String', formula_prototype_handler),
    },
    'calculations': {
        'id': ('String', string_handler),
        'modification_date': ('String', string_handler),
    }
}

optimade_valid_response_fields = {
    'structures': ['id', 'modification_date', 'elements',
                   'nelements', 'chemical_formula', 'formula_prototype'],
    'calculations': ['id', 'modification_date']
}
