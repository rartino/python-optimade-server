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

import datetime


def generate_entry_endpoint_reply(request, data):
    """
    This just returns a hardcoded introspection string.
    """

    data_part = []
    for d in data:
        attributes = dict(d)
        del attributes['id']
        del attributes['type']
        data_part += [{
            'attributes': attributes,
            'id': d['id'],
            'type': d['type'],
        }]

    response = {
        "links": {
            "base_url": request['baseurl'],
            # Pagination not supported yet (which is OK according to specification)
            "next": None
        },
        "data": data_part,
        "meta": {
            "query": {
                "representation": request['representation']
            },
            "api_version": request['version'],
            "time_stamp": datetime.datetime.now().isoformat(),
            "data_returned": len(data_part),
            "more_data_available": data.more_data_available,
        }        
    }

    # TODO: Add 'next' element in links for pagination, via info propagated in data
    #   Add "data_available" if available in data
    #   Fix more_data_available

    return response

