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

from __future__ import print_function

from example_sqlite3 import database
from translate import optimade_filter_to_sql, string_handler, integer_handler, elements_handler, chemical_formula_handler

database_column_mapper = {
    'structures': {
        'id': 'id',
        'local_id': 'local_id',
        'modification_date': 'modification_date',
        'elements': 'elements',
        'nelements': 'nelements',
        'chemical_formula': 'chemical_formula',
        'formula_prototype': 'formula_prototype'
    },
    'calculations': {
        'id': 'id',
        'modification_date': 'modification_date',
    }
}

database_table_mapper = {
    'structures': 'test_structures',
    'calculations': 'test_calculations'
}


def initialize():

    database.initalize()
    _setup_test_data()


def execute_query(tables, response_fields, response_limit, optimade_filter_ast=None, debug=False):

    result = optimade_filter_to_sql('sqlite3', optimade_filter_ast, tables, response_fields, database_table_mapper, database_column_mapper, response_limit)
    sql, parameters = result['sql'], result['parameters']

    # Just to show the results on screen
    # (DO NOT SEND STRINGS CONSTRUCTED THIS WAY TO A DATABASE, IT IS NOT SAFE.)
    display_sql = sql
    for repstr in parameters:
        if isinstance(repstr, str) or isinstance(repstr, u""):
            display_sql = display_sql.replace(':'+repstr, "'"+str(parameters[repstr])+"'")
        else:
            display_sql = display_sql.replace(':'+repstr, str(parameters[repstr]))

    if debug:
        print("==== SQL STRING: (note: values not displayed quoted correctly here)")
        print(display_sql)
        print("====")

    # Run the query    
    results = database.execute(sql, parameters)

    #if debug:
    #    print("==== SQL QUERY RESULT:")
    #    print("Number of results found:", len(results))
    #    for row in results:
    #        print(row)

    return results


def close():
    database.close()


def _setup_test_data():
    database.execute("create table structures (id, local_id, modification_date, elements, nelements, chemical_formula, formula_prototype)")

    structs = [
        {'id': 'st-1', 'local_id': 'st-1', 'modification_date': '2019-03-20 23:45',
         'elements': 'Al,Ga,Ti', 'nelements': 3, 'chemical_formula': 'Al3Ga2Ti3', 'formula_prototype': 'A3B2C3'},
        {'id': 'st-2', 'local_id': 'st-2', 'modification_date': '2019-03-20 23:45',
         'elements': 'Al,Ga', 'nelements': 2, 'chemical_formula': 'Al3Ga2', 'formula_prototype': 'A3B2'},
        {'id': 'st-3', 'local_id': 'st-3', 'modification_date': '2019-03-20 23:45',
         'elements': 'Al,N,Ga,Ti', 'nelements': 4, 'chemical_formula': 'Al3Ga2Ti3N2', 'formula_prototype': 'A3B2C3D2'},
        {'id': 'st-4', 'local_id': 'st-4', 'modification_date': '2019-03-20 23:45',
         'elements': 'B,C', 'nelements': 2, 'chemical_formula': 'B6C7', 'formula_prototype': 'A6B7'},
        {'id': 'st-5', 'local_id': 'st-5', 'modification_date': '2019-03-20 23:45',
         'elements': 'Al,C', 'nelements': 2, 'chemical_formula': 'Al3C6', 'formula_prototype': 'A3C6'},
        {'id': 'st-6', 'local_id': 'st-6', 'modification_date': '2019-03-20 23:45',
         'elements': 'Ga,Ti', 'nelements': 2, 'chemical_formula': 'Ga26Ti12', 'formula_prototype': 'A26B12'},
        {'id': 'st-7', 'local_id': 'st-7', 'modification_date': '2019-03-20 23:45',
         'elements': 'C', 'nelements': 1, 'chemical_formula': 'C60', 'formula_prototype': 'A60'},        
    ]

    for struct in structs:
        database.execute("insert into structures values (:id,:local_id,:modification_date,:elements,:nelements,:chemical_formula,:formula_prototype)", struct)

    database.execute("create table calculations (id, local_id, modification_date)")

    calcs = [
        {'id': 'calc-1', 'local_id': 'calc-1', 'modification_date': '2019-03-21 23:45'},
        {'id': 'calc-2', 'local_id': 'calc-1', 'modification_date': '2019-03-22 23:45'},
        {'id': 'calc-3', 'local_id': 'calc-1', 'modification_date': '2019-03-23 23:45'},
        {'id': 'calc-4', 'local_id': 'calc-1', 'modification_date': '2019-03-24 23:45'},
        {'id': 'calc-5', 'local_id': 'calc-1', 'modification_date': '2019-03-25 23:45'},
        {'id': 'calc-6', 'local_id': 'calc-1', 'modification_date': '2019-03-26 23:45'},
        {'id': 'calc-7', 'local_id': 'calc-1', 'modification_date': '2019-03-27 23:45'}
    ]

    for calc in calcs:
        database.execute("insert into calculations values (:id,:local_id,:modification_date)", calc)

    database.commit()

