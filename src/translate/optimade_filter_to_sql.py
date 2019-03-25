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
This file provides functions to translate an OPTIMaDe filter string into an SQL query. 
'''

from __future__ import print_function
import re
from pprint import pprint

from .error import TranslatorError

supported_dialects = ['sqlite3']


def optimade_filter_to_sql(dialect, filter_ast, tables, response_fields, tables_mapper, columns_mapper, response_limit, indent=True):

    if dialect not in supported_dialects:
        raise Exception("optimade_filter_to_sql: Requested dialect is not supported: "+str(dialect))

    response_fields = set(response_fields)
    if 'id' in response_fields:
        response_fields.remove('id')
    if 'type' in response_fields:
        response_fields.remove('type')

    sql = {
        'dialect': dialect,
        'parameter_count': 0,
        'parameters': {}        
    }

    sqlstr = ""
    sql_tbl_strs = []

    for table in tables:
        sql_tbl_str = ""
        if len(response_fields) > 0:
            sql_tbl_str += "SELECT "+",".join(response_fields)+", '"+table + "' AS type, id"+" \n"
        else:
            if len(tables) > 1:
                raise Exception("Must give response_fields if giving more than one table to union.")
            else:
                sql_tbl_str += "SELECT *,'"+tables_mapper[table]+"' AS type \n"

        sql_tbl_str += sqlstr + "FROM " + table + " \n" 

        if filter_ast is not None:
            qs = optimade_filter_to_sql_recurse(filter_ast, sql, columns_mapper[table], optimade_valid_columns_per_table[table], indent=indent)
            sql_tbl_str += "WHERE " + qs + " \n"

        sql_tbl_strs += [sql_tbl_str]

    sqlstr = " UNION \n".join(sql_tbl_strs)

    if response_limit is not None:
        sqlstr += "LIMIT "+str(response_limit)+" \n"

    return {'sql': sqlstr, 'parameters': sql['parameters']}


def optimade_filter_to_sql_recurse(node, sql, columns_mapper, columns_handlers, indent=True, recursion=0):

    indentstr = "  "+"  "*recursion

    qs = ""
    if node[0] in ['AND', 'OR']:            
        qs += "(\n"+indentstr+"  " if indent else "("
        qs += optimade_filter_to_sql_recurse(node[1], sql, columns_mapper, columns_handlers, indent=indent, recursion=recursion+1)
        qs += "\n"+indentstr+")" if indent else ")"
        qs += " "+node[0]+" "
        qs += "(\n"+indentstr+"  " if indent else "("
        qs += optimade_filter_to_sql_recurse(node[2], sql, columns_mapper, columns_handlers, indent=indent, recursion=recursion+1)
        qs += "\n"+indentstr+")" if indent else ")"        
    elif node[0] in ['NOT']:            
        qs += "(\n"+indentstr+"  " if indent else "("
        qs += optimade_filter_to_sql_recurse(node[1], sql, columns_mapper, columns_mapper, columns_handlers, indent=indent, recursion=recursion+1)
        qs += "\n"+indentstr+")" if indent else ")"
    elif node[0] in ['>', '>=', '<', '<=', '=', '!=']:
        op = node[0]
        left = node[1]
        right = node[2]
        if left[0] == 'Value' and right[0] == 'Value':
            # This is apparently allowed in the grammar? **            
            qs += unknown_types_handler(op, left[1], right[1], sql)
        else:
            if left[0] == 'Identifier' and right[0] == 'Value':
                left, right = right, left
            assert(left[0] == 'Identifier')
            sql_column = columns_mapper[left[1]] 
            argtype, handler = columns_handlers[left[1]] 
            assert(right[0] == argtype)
            value = right[1]
            qs += handler(sql_column, op, value, sql)
    else:
        pprint(node)
        raise TranslatorError("Unexpected translation error", 500, "Internal server error.")
    return qs


_sql_opmap = {'!=': '<>', '>': '>', '<': '<', '=': '=', '<=': '<=', '>=': '>='}


def _prep(val, sql):
    parameter = 'l'+str(sql['parameter_count']+1)
    sql['parameter_count'] += 1
    sql['parameters'][parameter] = val
    return ':'+parameter


def string_handler(entry, op, value, sql):
    sql_op = _sql_opmap[op]
    value = value[1:-1]
    parameter = _prep(value, sql)
    return entry + " "+sql_op+" " + parameter


def integer_handler(entry, op, value, sql):
    sql_op = _sql_opmap[op]
    parameter = _prep(int(value), sql)
    return entry + " "+sql_op+" " + parameter


def elements_handler(entry, op, value, sql):

    if op != '=':
        raise TranslatorError("Elements can only be compared with equals operator.", 400, "Bad request.")

    segments = []
    value = value[1:-1]
    els = value.split(",")
    for el in els:
        el = el.strip()
        segment = ""
        parameter = _prep('%,'+el+',%', sql)
        segment += entry + " LIKE "+parameter
        parameter = _prep(el+',%', sql)
        segment += " OR "+entry + " LIKE "+parameter
        parameter = _prep('%,'+el, sql)
        segment += " OR "+entry + " LIKE "+parameter
        segments += [segment]
    return "("+") AND (".join(segments)+")"


# Assumes the formula is stored according to element name in the database
def chemical_formula_handler(entry, op, value, sql):

    if op != '=':
        raise TranslatorError("Chemical formulas can only be compared with equals operator.", 400, "Bad request.")

    value = value[1:-1]
    segments = sorted(re.findall('[A-Z][a-z]?[0-9]*', value))
    sorted_formula = "".join(segments)
    parameter = _prep(sorted_formula, sql)
    return entry + " = " + parameter

# Assumes the formula is stored according to element name in the database


def formula_prototype_handler(entry, op, value, sql):

    if op != '=':
        raise TranslatorError("Formula prototypes can only be compared with equals operator.", 400, "Bad request.")

    value = value[1:-1]
    try:
        segments = sorted((int(x[1]), x[0]) for x in re.findall('([A-Z][a-z]?)([0-9]*)', value))
    except ValueError:
        raise TranslatorError("Misformed formula_prototype request.", 400, "Bad request.")
    sorted_formula = "".join([x[1]+str(x[0]) for x in segments])
    parameter = _prep(sorted_formula, sql)
    return entry + " = " + parameter


def unknown_types_handler(val1, op, val2, sql):
    sql_op = _sql_opmap[op]
    if (val1.startswith('"') and val1.endswith('"')): 
        val1 = val1[1:-1]
    if (val2.startswith('"') and val2.endswith('"')): 
        val2 = val2[1:-1]
    param1 = _prep(val1, sql)
    param2 = _prep(val2, sql)
    return param1 + " "+sql_op+" " + param2


optimade_valid_columns_per_table = {
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




