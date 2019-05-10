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

# TODO: This should be replaced with json schema validation when we have a proper schema for the json output
from .response import validate_response
from .request import request, RequestError

def validate_base_info(json):

    result = validate_response(json)

    if json is None:
        # Error for this is handled by validate_response
        return result

    allowed_data = {'type', 'id', 'attributes'}
    # Note: specification bug: specification shows in the example available_endpoints, but it isn't allowed according to the spec
    allowed_attributes = {'api_version','available_api_versions','formats','entry_types_by_format','available_endpoints'}
    
    # No neet to return errors if these are missing, since validate_response handles that
    if 'meta' in json:
        if 'data_returned' in json['meta']:
            if json['meta']['data_returned'] != 0:
                result['error'] += [{'description':'meta->data_returned is not zero'}]

    if 'data' not in json:
        result['error'] += [{'description':'missing data member'}]
    else:
        data = json['data']
        # It is unclear in the specification if data has to be a list
        if isinstance(data, list):
            if len(data)!=1:
                result['error'] += [{'description':'data is a list, but the length is not = 1'}]
            data = data[0]
            
        if not isinstance(data, dict):
            result['error'] += [{'description':'data is not either a dict, or, a list with one dict'}]
        else:
            if 'type' not in data:
                result['error'] += [{'description':'missing data->type member'}]
            else:
                if data['type'] != "info":
                    result['error'] += [{'description':'data->type is not info, it is:'+str(data)}]

            if 'id' not in data:
                result['error'] += [{'description':'missing data->id member'}]
            else:
                if data['id'] != "/":
                    result['error'] += [{'description':'data->id is not "/"'}]

            if 'attributes' not in data:
                result['error'] += [{'description':'missing data->attributes member'}]
            else:
                attributes=data['attributes']
                if 'api_version' not in attributes:
                    result['error'] += [{'description':'missing data->attributes->api_version member'}]
                elif attributes['api_version'] != 'v0.9.5':
                    result['error'] += [{'description':'data->attributes->api_version is not "v0.9.5"'}]

                remaining_attributes = {key: attributes[key] for key in attributes if ((key not in allowed_attributes) and (key[0] != '_'))}
                if len(remaining_attributes) > 0:
                    result['error'] += [{'description':'data->attributes contains unallowed keys: '+", ".join([str (x) for x in remaining_attributes])}]        

            if 'available_api_versions' not in attributes:
                result['error'] += [{'description':'missing data->attributes->available_api_versions'}]
            else:
                #TODO: Validate available_api_versions
                pass

            if 'formats' not in attributes:
                result['error'] += [{'description':'missing data->attributes->formats member'}]
            else:
                #TODO Validate formats
                pass

            if 'entry_types_by_format' not in attributes:
                result['error'] += [{'description':'missing data->attributes->entry_types_by_format member'}]
            else:
                #TODO Validate formats
                pass        

            remaining_data = {key: data[key] for key in data if ((key not in allowed_data) and (key[0] != '_'))}
            if len(remaining_data) > 0:
                result['error'] += [{'description':'data memeber contains unallowed keys'}]        
            
    return result


def validate_base_info_request(base_url, relurl='/info'):
    try:
        result = request(base_url+relurl)
        return validate_base_info(result['response'])
    except RequestError as e:
        return {'error':str(e), 'warning':[], 'note':[]}
        


if __name__ == '__main__':
    import pprint
    
    pprint.pprint(validate_base_info_request("http://localhost:8080"))
