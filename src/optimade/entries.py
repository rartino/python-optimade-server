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

entry_info = {
    'structures': {
        'descripion': 'a structure',
        'properties': {
            'id': {
                'description': "An entry's ID."
            },
            'modification_date': {
                'description': "A date representing when the entry was last modified."
            },
            'elements': {
                'description': "names of elements found in the structure."
            },
            'nelements': {
                'description': "The number of elements found in a structure."
            },
            'chemical_formula': {
                'description': "The chemical formula for a structure."
            },
            'formula_prototype': {
                'description': "The formula prototype obtained by sorting elements by the occurrence number in the reduced chemical formula and replace them with subsequent alphabet letters A, B, C and so on."
            }
        }
    },
    'calculations': {
        'descripion': 'a calculation',
        'properties': {
            'id': {
                'description': "An entry's ID."
            },
            'modification_date': {
                'description': "A date representing when the entry was last modified."
            },
        }
    }
}

all_entries = entry_info.keys()

properties_by_entry = dict([(x, entry_info[x]['properties']) for x in entry_info])

# In the future, not all properties may be valid response fields
valid_response_fields = properties_by_entry

valid_endpoints = ['info', 'all'] + all_entries + [x+"/info" for x in all_entries] + ['']

