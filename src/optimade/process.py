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

from pprint import pprint

from .entries import all_entries, valid_response_fields
from .validate import validate
from .info_endpoint import generate_info_endpoint_reply, generate_entry_info_endpoint_reply, generate_base_endpoint_reply
from .entry_endpoint import generate_entry_endpoint_reply
from .error import OptimadeError
from parse import ParserSyntaxError, parse_optimade_filter


def process(baseurl, relurl, query, query_function, debug=False):

    if debug:
        print("==== OPTIMADE REQUEST FOR:", relurl, "WITH PARAMETERS:")
        pprint(query)
        print("====")

    validated_parameters = validate(relurl, query)

    if debug:
        print("==== VALIDATED PARAMETERS:")
        pprint(validated_parameters)
        print("====")

    endpoint = validated_parameters['endpoint']
    if endpoint == '':
        response = generate_base_endpoint_reply()

    elif endpoint == 'info':
        response = generate_info_endpoint_reply(baseurl, validated_parameters['version'])

    elif endpoint in all_entries or endpoint == 'all':

        response_fields = validated_parameters['response_fields']

        if endpoint != 'all':
            tables = [endpoint]
        else:
            tables = all_entries
            if len(response_fields) == 0:
                response_fields = set(valid_response_fields[all_entries[0]])
                for entry in all_entries:
                    response_fields = response_fields.intersection(set(valid_response_fields[entry]))

        input_string = None
        filter_ast = None
        if 'request_id' in validated_parameters:
            input_string = 'filter=id="'+validated_parameters['request_id']+'"'
            filter_ast = ('=', ('Identifier', 'id'), ('String', '"'+validated_parameters['request_id']+'"'))
        elif 'filter' in validated_parameters:
            input_string = validated_parameters['filter']

        if input_string is not None:
            if filter_ast is None:
                try:
                    filter_ast = parse_optimade_filter(input_string)
                except ParserSyntaxError as e:
                    raise OptimadeError(str(e), 400, "Bad request")

            if debug:
                print("==== FILTER STRING PARSE RESULT:")
                pprint(filter_ast)
                print("====")

            result = query_function(tables, response_fields, validated_parameters['response_limit'], filter_ast, debug=debug)
            response = generate_entry_endpoint_reply(result)
        else:
            result = query_function(tables, response_fields, validated_parameters['response_limit'], debug=debug)

            response = generate_entry_endpoint_reply(result)

        if debug:
            print("==== END RESULT")
            pprint(response)
            print("===============")

    elif endpoint.endswith("info"):
        base, _sep, info = endpoint.rpartition("/")
        assert(info == "info")
        if base in all_entries:
            response = generate_entry_info_endpoint_reply(base)            
        else:
            raise OptimadeError("Internal error: unexpected endpoint.", 500, "Internal server error")

    else:
        raise OptimadeError("Internal error: unexpected endpoint.", 500, "Internal server error")

    return response
