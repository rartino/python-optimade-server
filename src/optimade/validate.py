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

from .entries import all_entries, valid_endpoints, valid_response_fields
from .error import OptimadeError
from .versions import optimade_supported_versions, optimade_default_version

def validate(relurl, query):
    validated_parameters = {'response_limit': 50, 'endpoint': None, 'response_fields': []}

    if 'response_format' in query and 'response_format' != 'json':
        raise OptimadeError("Requested response_format not supported.", 400, "Bad request")

    if 'response_limit' in query:
        try:
            validated_parameters['response_limit'] = int(query['response_limit'])
        except ValueError:
            raise OptimadeError("Cannot interprete response_limit.", 400, "Bad request")
        if validated_parameters['response_limit'] > 50:
            validated_parameters['response_limit'] = 50

    endpoint = relurl.rstrip("/")

    potential_optimade_version, _sep, rest = endpoint.partition('/')    
    
    if len(potential_optimade_version) > 2 and potential_optimade_version[0] == 'v' and potential_optimade_version[1] in "0123456789":
        if potential_optimade_version in optimade_supported_versions:
            validated_parameters['version'] = optimade_supported_versions[potential_optimade_version]
            endpoint = rest
        else:
            raise OptimadeError("Unsupported version requested", 400, "Bad request")

    if 'version' not in validated_parameters:
        validated_parameters['version'] = optimade_default_version
        
        
    if endpoint in valid_endpoints:
        # Defensive programming; don't trust '=='/in to be byte-for-byte equivalent,
        # so don't use the insecure string from the user
        validated_parameters['endpoint'] = valid_endpoints[valid_endpoints.index(endpoint)]
    else:
        endpoint, _sep, request_id = endpoint.rpartition('/')
        if endpoint in valid_endpoints:
            # Defensive programming; don't trust '=='/in to be byte-for-byte equivalent,
            # so don't use the insecure string from the user
            validated_parameters['endpoint'] = valid_endpoints[valid_endpoints.index(endpoint)]
            # Only allow printable ascii characters in id; this is not in the standard, but your
            # database really should adhere to it or you are doing weird things.
            if all(ord(c) >= 32 and ord(c) <= 126 for c in request_id):
                validated_parameters['request_id'] = request_id
            else:
                raise OptimadeError("Unexpected characters in entry id.", 400, "Bad request") 

    if validated_parameters['endpoint'] is None:
        raise OptimadeError("Request for invalid endpoint.", 400, "Bad request")

    if 'response_fields' in query:
        response_fields = [x.strip() for x in query['response_fields'].split(",")]
        for response_field in response_fields:
            if response_field in valid_response_fields[endpoint]:
                validated_parameters['response_fields'] += [valid_response_fields[endpoint][valid_response_fields[endpoint].index(response_field)]]

    # Validating the filter string is deferred to its parser
    if 'filter' in query:
        validated_parameters['filter'] = "filter="+query['filter']

    return validated_parameters
