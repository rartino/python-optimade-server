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

from pprint import pprint

from .entries import all_entries, valid_response_fields
from .validate import validate_optimade_request
from .info_endpoint import generate_info_endpoint_reply, generate_entry_info_endpoint_reply, generate_base_endpoint_reply
from .entry_endpoint import generate_entry_endpoint_reply
from .error import OptimadeError
from parse import ParserSyntaxError, parse_optimade_filter
from translate import TranslatorError


def process(request, query_function, debug=False):
    """
    Process an optimade query.

    Args:
      request: a dict with these entries: 
                   baseurl (required): the base url that serves the OPTIMaDe API. 
                   representation (mandatory): the string with the part of the URL that follows the base URL. This must always be provided, because
                        the OPTIMaDe specification requires this to be part of the output in the meta section (meta -> query -> representation).
                   relurl (optional): the part of the URL that follows the base URL but without query parameters.
                        Include this if the web-serving framework provides this, i.e., if it splits off the query part for you.
                   endpoint (optional): the endpoint being requested 
                   request_id (optional): a specific entry id being requested.
                   querystr (optional): a string that defines the query parameters that follows the base URL and the relurl and a single '?'.   
                   query (optional): a dictionary representation of the query part of the URL.   
          missing information is derived from the 'representation' string.

      query_function: a callback function of signature
                         query_function(entries, response_fields, response_limit, filter_ast, debug)
                      with:
                         entries: list of optimade entries to run the query for, usually just the entry type requested by the end point.
                         response_fields: which fields should be present in the output
                         response_limit: the maximum number of results to return
                         filter_ast: an abstract syntax tree representing the optimade filter requested
                         debug: if set to true, print debug information to stdout.
                      returns an OptimadeResults object.

    """
    
    if debug:
        print("==== OPTIMADE REQUEST FOR:", request['representation'])

    validated_request = validate_optimade_request(request)
    baseurl = validated_request['baseurl']
    endpoint = validated_request['endpoint']
    request_id = validated_request['request_id']
    version = validated_request['version']        
    validated_parameters = validated_request['query']

    if debug:
        print("==== VALIDATED ENDPOINT, REQUEST_ID, AND PARAMETERS:")
        print("ENDPOINT:",endpoint)
        print("REQUEST_ID:",request_id)
        pprint(validated_parameters)
        print("====")

    if endpoint == '':
        response = generate_base_endpoint_reply(validated_request)

    elif endpoint == 'info':
        response = generate_info_endpoint_reply(validated_request)

    elif endpoint in all_entries or endpoint == 'all':

        response_fields = validated_parameters['response_fields']

        if endpoint != 'all':
            entries = [endpoint]
        else:
            entries = all_entries
            if len(response_fields) == 0:
                response_fields = set(valid_response_fields[all_entries[0]])
                for entry in all_entries:
                    response_fields = response_fields.intersection(set(valid_response_fields[entry]))

        input_string = None
        filter_ast = None
        if request_id is not None:
            input_string = 'filter=id="'+request_id+'"'
            filter_ast = ('=', ('Identifier', 'id'), ('String', '"'+request_id+'"'))
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

            try:
                results = query_function(entries, response_fields, validated_parameters['response_limit'], filter_ast, debug=debug)
            except TranslatorError as e:
                raise OptimadeError(str(e), e.response_code, e.response_msg)

            response = generate_entry_endpoint_reply(validated_request, results)
        else:
            results = query_function(entries, response_fields, validated_parameters['response_limit'], debug=debug)

            response = generate_entry_endpoint_reply(validated_request, results)

        if debug:
            print("==== END RESULT")
            pprint(response)
            print("===============")

    elif endpoint.endswith("info"):
        base, _sep, info = endpoint.rpartition("/")
        assert(info == "info")
        if base in all_entries:
            response = generate_entry_info_endpoint_reply(validated_request, base)            
        else:
            raise OptimadeError("Internal error: unexpected endpoint.", 500, "Internal server error")

    else:
        raise OptimadeError("Internal error: unexpected endpoint.", 500, "Internal server error")

    return response
