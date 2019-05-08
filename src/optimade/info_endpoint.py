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

from .entries import entry_info, all_entries
from .versions import optimade_supported_versions


def generate_info_endpoint_reply(request):
    """
    This just returns a hardcoded introspection string.
    """
    available_api_versions = {}
    for ver in optimade_supported_versions:
        available_api_versions[optimade_supported_versions[ver]] = baseurl + ver

    response = {
        "links": {
            "base_url": request['baseurl']
            },
        "data": [
            {
                "type": "info",
                "id": "/",
                "attributes": {
                    "api_version": 'v'+version,
                    "available_api_versions": available_api_versions,
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
        ],
        "meta": {
            "query": {
                "representation": request['representation']
            },
            "api_version": request['version'],
            "time_stamp": datetime.datetime.now().isoformat(),
            "data_returned": 0,
            "more_data_available": False,
         }
    }
    return response


def generate_entry_info_endpoint_reply(request, entry):

    return {
        "links": {
            "base_url": request['baseurl']
            },
        "data": [
            entry_info[entry]
        ],
        "meta": {
            "query": {
                "representation": request['representation']
            },
            "api_version": request['version'],
            "time_stamp": datetime.datetime.now().isoformat(),
            "data_returned": 0,
            "more_data_available": False,
         }        
    }


def generate_base_endpoint_reply(request):

    return {
        "links": {
            "base_url": request['baseurl']
            },
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
        ],
        "meta": {
            "query": {
                "representation": request['representation']
            },
            "api_version": request['version'],
            "time_stamp": datetime.datetime.now().isoformat(),
            "data_returned": 0,
            "more_data_available": False,
         }        
    }

