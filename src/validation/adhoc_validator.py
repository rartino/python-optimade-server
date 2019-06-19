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

from .request import request, RequestError

def adhoc_validate_response(json, expect_error=False, init_result=None):

    if init_result is None:
        result = {'error':[], 'warning':[], 'note':[]}
    else:
        result = init_result

    allowed = {'errors', 'links', 'meta', 'data', 'include'}
    allowed_links = {'next','base_url'}
    allowed_meta = {'query', 'api_version', 'time_stamp', 'data_returned', 'more_data_available', 'data_available', 'last_id', 'response_message', 'provider'}

    if json is None:
        result['error'] += [{'description':'output is null'}]
        return result
        
    # ERROR section
    if 'errors' in json and not expect_error:        
        result['note'] += [{'description':'unexpected error member in response to base_info'}]

    if 'errors' not in json and expect_error:        
        result['note'] += [{'description':'missing expected error member in response to base_info'}]

    if expect_error:
        return

    # LINKS SECTION
    if 'links' not in json:
        result['error'] += [{'error':'response to base_info missing links member'}]
    else:
        links = json['links']
        if 'base_url' not in links:
            result['note'] += [{'description':'links member missing base_url'}]
            
        remaining_links = {key: links[key] for key in links if ((key not in allowed_links) and (key[0] != '_'))}
        if len(remaining_links) > 0:
            result['error'] += [{'description':'links member contains unallowed keys: '+str(remaining_links)}]        

            
    # META SECTION            
    if 'meta' not in json:
        result['error'] += [{'error':'response to base_info missing meta member'}]
    else:
        meta = json['meta']
        if 'query' not in meta:
            result['error'] += [{'description':'meta member missing query member'}]
        else:
            if 'representation' not in meta['query']:
                result['error'] += [{'description':'meta -> query member missing representation member'}]
            
        if 'api_version' not in meta:
            result['error'] += [{'description':'meta member is missing api_version member'}]
        elif meta['api_version'] != '0.9.5':
                result['error'] += [{'description':'meta->api_version is not 0.9.5'}]
                
        if 'time_stamp' not in meta:
            result['error'] += [{'description':'meta member is missing api_version member'}]
        else:
            pass
            # TODO Add validation of ISO 8601

        if 'data_returned' not in meta:
            result['error'] += [{'description':'meta member is missing data_returned member'}]
        elif not isinstance(meta['data_returned'], int):
            result['error'] += [{'description':'meta->data_returned is not integer'}]

        if 'more_data_available' not in meta:
            result['error'] += [{'description':'meta member is missing more_data_available member'}]
        elif not isinstance(meta['more_data_available'], bool):
            result['error'] += [{'description':'meta->data_returned is not bool'}]

        remaining_meta = {key: meta[key] for key in meta if ((key not in allowed_meta) and (key[0] != '_'))}
        if len(remaining_meta) > 0:
            result['error'] += [{'description':'meta member contains unallowed keys: '+str(remaining_meta)}]        
            
    if 'include' in json:
        include = json['include']
        if not isinstance(meta['data_returned'], list):
            result['error'] += [{'description':'include member is not a list'}]

    remaining = {key: json[key] for key in json if ((key not in allowed) and (key[0] != '_'))}
    if len(remaining) > 0:
        result['error'] += [{'description':'response contains unallowed keys'}]

    return result


def adhoc_fetch_and_validate(base_url, test, init_result = None):

    if init_result is None:
        result = {'error':[], 'warning':[], 'note':[]}
    else:
        result = init_result
        
    try:
        output = request(base_url+test['relurl'])
        return adhoc_validate_response(output['response'])
        return result
    
    except RequestError as e:
        result['error'] += [{'description':str(e)}]
        return result

