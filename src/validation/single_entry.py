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

from .request import request

def prepare_single_entry(base_url, test, init_result = None):

    if init_result is None:
        result = {'error':[], 'warning':[], 'note':[]}
    else:
        result = init_result
        
    try:
        output = request(base_url+test['relurl'])
        json = output['response']
        
        if json is None:
            result['error'] += [{'description':'output is null'}]
            return result
        
        if 'data' not in json:
            result['error'] += [{'description':'missing data member'}]
        else:
            data = json['data']
            # It is unclear in the specification if data has to be a list
            if isinstance(data, list):
                if not len(data)>0:
                    result['error'] += [{'description':'no data returned'}]
                data = data[-1]

                if 'id' not in data:
                    result['error'] += [{'description':'data->id missing'}]
                else:
                    lastid = data['id']
                    if not (isinstance(lastid,type('')) or isinstance(lastid,type(u''))):
                        result['error'] += [{'description':'data->id is not a string: '+str(type(lastid))}]
                    test['relurl'] = test['relurl'] + "/" + data['id']
                    return result
                
        test['stop'] = True    
        return result
    
    except RequestError as e:
        test['stop'] = True
        result['error'] += [{'description':str(e)}]
        return result
        
