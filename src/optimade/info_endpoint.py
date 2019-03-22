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

from optimade.entries import entry_info, all_entries


def generate_info_endpoint_reply(baseurl):
    """
    This just returns a hardcoded introspection string.
    """

    response = {    
        "data": [
            {
                "type": "info",
                "id": "/",
                "attributes": {
                    "api_version": "v0.9",
                    "available_api_versions": {
                        "0.9.5": baseurl+"v0.9/",
                    },
                    "formats": [
                        "json"
                    ],
                    "entry_types_by_format": {
                        "json": [
                            "structure",
                            "calculation"
                        ],
                    },
                    "available_endpoints": [
                        "entry",
                        "all",
                        "info"
                    ]
                }
            }
        ]
    }
    return response


def generate_entry_info_endpoint_reply(entry):

    return {
        "data": [
            entry_info[entry]
        ]
    }


def generate_base_endpoint_reply():

    return {
        "data": [
            {
                "type": "OPTIMaDe base url",
                "id": "/",
                "attributes": {
                    "available_endpoints": [
                        all_entries
                    ]
                }
            }
        ]
    }

