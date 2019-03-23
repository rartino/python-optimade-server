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

