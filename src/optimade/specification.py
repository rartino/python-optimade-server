#!/usr/bin/env python
#
# This specific file is a mere re-formatting of information in
# the OPTIMaDe specifaction [http://www.optimade.org/].
#
# Formally, the author makes a Public Domain Dedication
# according to CC0 1.0 Universal (CC0 1.0)
#   https://creativecommons.org/publicdomain/zero/1.0/
#
# (Note, this only applies to this one specific file.)
#

entry_info = {
    'structures': {
        'descripion': 'a structure'
        'properties': {
            'id': {
                'description': "An entry's ID."
            },
            'local_id': {
                'description': "the entry's local database ID"
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
            'chemical_formula', {
                'description': "The chemical formula for a structure."
            },
            'formula_prototype', {
                'description': "The formula prototype obtained by sorting elements by the occurrence number in the reduced chemical formula and replace them with subsequent alphabet letters A, B, C and so on."
            }
        }
    }
    'calculation': {
        'descripion': 'a calculation'
        'properties': {
            'id': {
                'description': "An entry's ID."
            },
            'local_id': {
                'description': "the entry's local database ID"
            },
            'modification_date': {
                'description': "A date representing when the entry was last modified."
            },
        }
    }
}

valid_properties_by_entry = dict([(x, entry_info[x]['properties']) for x in entry_info])

valid_endpoints = ['info', 'all'] + all_entries + [x+"/info" for x in entry_info]

