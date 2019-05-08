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
from translate import optimade_filter_to_sql
from testdata import get_test_structures

database = None

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
        'local_id': 'local_id',
        'modification_date': 'modification_date',
    }
}

database_table_mapper = {
    'structures': 'test_structures',
    'calculations': 'test_calculations'
}

class Results(object):
    def __init__(self, cur, limit):
        self.cur = cur
        self.limit = limit
        self.count = 0
        self.more_data_available = True
        
    def __iter__(self):
        return self

    def __next__(self):
        try:
            row = next(self.cur)
            result = dict([(name[0],d) for name,d in zip(self.cur.description, row)])
        except StopIteration:
            self.more_data_available = False
            self.cur.close()
            self.cur = None
            raise StopIteration
            
        if self.limit is not None and self.count == self.limit:
            self.more_data_available = True
            self.cur.close()
            self.cur = None
            raise StopIteration

        self.count += 1
        
        return result

    def __del__(self):
        if self.cur is not None:
            self.cur.close()
    
    # Python 2 compability
    def next(self):
        return self.__next__()


def initialize(db = None):
    global database
    
    if db is None:
        database = default_database.Database()
    else:
        database = db
    _setup_test_data()


def execute_query(entries, response_fields, response_limit, optimade_filter_ast=None, debug=False):

    # Ask for one more row than required, that way we can fill out 'has_more_data'
    result = optimade_filter_to_sql('sqlite3', optimade_filter_ast, entries, response_fields, database_table_mapper, database_column_mapper)
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
    results = database.execute(sql, parameters, response_limit)
    
    #if debug:
    #    print("==== SQL QUERY RESULT:")
    #    print("Number of results found:", len(results))
    #    for row in results:
    #        print(row)

    return Results(results,response_limit)


def close():
    database.close()


def _setup_test_data():
    database.execute("drop table if exists structures")
    database.execute("create table structures (id, local_id, modification_date, elements, nelements, chemical_formula, formula_prototype)")

    teststructs = get_test_structures()
    
    for teststruct in teststructs:

        struct = {}

        struct['id'] = teststruct.id
        struct['local_id'] = teststruct.id
        struct['modification_date'] = teststruct.modification_date
        struct['nelements'] = teststruct.nelements
        
        segments = sorted(re.findall('[A-Z][a-z]?[0-9]*', teststruct.chemical_formula))
        struct['chemical_formula'] = "".join(segments)

        struct['formula_prototype'] = teststruct.formula_prototype
        struct['elements'] = teststruct.elements

        database.execute("insert into structures values (:id,:local_id,:modification_date,:elements,:nelements,:chemical_formula,:formula_prototype)", struct)

    database.execute("drop table if exists calculations")        
    database.execute("create table calculations (id, local_id, modification_date)")

    calcs = [
        {'id': 'calc-1', 'local_id': 'calc-1', 'modification_date': '2019-03-21 23:45'},
        {'id': 'calc-2', 'local_id': 'calc-2', 'modification_date': '2019-03-22 23:45'},
        {'id': 'calc-3', 'local_id': 'calc-3', 'modification_date': '2019-03-23 23:45'},
        {'id': 'calc-4', 'local_id': 'calc-4', 'modification_date': '2019-03-24 23:45'},
        {'id': 'calc-5', 'local_id': 'calc-5', 'modification_date': '2019-03-25 23:45'},
        {'id': 'calc-6', 'local_id': 'calc-6', 'modification_date': '2019-03-26 23:45'},
        {'id': 'calc-7', 'local_id': 'calc-7', 'modification_date': '2019-03-27 23:45'}
    ]

    for calc in calcs:
        database.execute("insert into calculations values (:id,:local_id,:modification_date)", calc)

    database.commit()

