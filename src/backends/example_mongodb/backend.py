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
import re

from . import database as default_database
from translate import optimade_filter_to_mongodb
from testdata import get_test_structures

database = None

database_column_mapper = {
    'structures': {
        'id': '_id',
        'local_id': 'local_id',
        'modification_date': 'modification_date',
        'elements': 'elements',
        'nelements': 'nelements',
        'chemical_formula': 'chemical_formula',
        'formula_prototype': 'formula_prototype'
    },
    'calculations': {
        'id': '_id',
        'modification_date': 'modification_date',
    }
}

database_table_mapper = {
    'structures': 'test_structures',
    'calculations': 'test_calculations'
}


def initialize(db = None):
    global database
    
    if db is None:
        database = default_database.Database()
    else:
        database = db
    _setup_test_data()


def execute_query(collections, response_fields, response_limit, optimade_filter_ast=None, debug=False):

    result = optimade_filter_to_mongodb('mongodb', optimade_filter_ast, collections, response_fields, database_table_mapper, database_column_mapper, response_limit)
    query = result['query']

    if debug:
        print("==== MONGODB QUERY:")
        print(query)
        print("====")

    # Run the query    
    results = database.find(sql, parameters)

    return results


def close():
    database.close()


def _setup_test_data():

    database.empty_database()

    teststructs = get_test_structures()

    structs = []
    
    for teststruct in teststructs:

        struct = {}

        struct['_id'] = teststruct.id
        struct['local_id'] = teststruct.id
        struct['modification_date'] = teststruct.modification_date
        struct['nelements'] = teststruct.nelements
        struct['chemical_formula'] = teststruct.chemical_formula
        struct['formula_prototype'] = teststruct.formula_prototype
        struct['elements'] = teststruct.elements

        structs += [struct]

    database.insert_many('structures',structs)

    calcs = [
        {'_id': 'calc-1', 'local_id': 'calc-1', 'modification_date': '2019-03-21 23:45'},
        {'_id': 'calc-2', 'local_id': 'calc-2', 'modification_date': '2019-03-22 23:45'},
        {'_id': 'calc-3', 'local_id': 'calc-3', 'modification_date': '2019-03-23 23:45'},
        {'_id': 'calc-4', 'local_id': 'calc-4', 'modification_date': '2019-03-24 23:45'},
        {'_id': 'calc-5', 'local_id': 'calc-5', 'modification_date': '2019-03-25 23:45'},
        {'_id': 'calc-6', 'local_id': 'calc-6', 'modification_date': '2019-03-26 23:45'},
        {'_id': 'calc-7', 'local_id': 'calc-7', 'modification_date': '2019-03-27 23:45'}
    ]

    database.insert_many('calculations',calcs)

