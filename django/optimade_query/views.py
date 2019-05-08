# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'src'))

from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from django.db import connections
import json
import optimade

import backends.example_sqlite3 as backend
from webserver import JsonapiError, check_jsonapi_header_requirements

_indent_json = True

if _indent_json:
    json_dumps_params={'indent': 4}
else:
    json_dumps_params={}

class Database(object): 

    def __init__(self):
        pass
        
    def execute(self,sql, parameters={}, limit=None):
        cur = connections['default'].cursor()
        if limit is not None:
            # Ask for limit + 1, so that the result set can know if there is more data available than was returned
            results = cur.execute(sql + "LIMIT "+str(limit+1), parameters) 
        else:
            results = cur.execute(sql, parameters)        
        return results

    def commit(self):
        return True
            
    def close(self):
        return

backend.initialize(db=Database())

# Create your views here.

def _django_request_to_optimade_request(request):

    querystr = request.META['QUERY_STRING']

    optimade_request = {}
    optimade_request['url'] = request.build_absolute_uri()
    optimade_request['scheme'] = request.scheme
    optimade_request['netloc'] = request.get_host()
    optimade_request['path'] = request.get_full_path()
    optimade_request['querystr'] = querystr
    optimade_request['port'] = request.get_port()
    optimade_request['baseurl'] = reverse('base_endpoint', request=request)
    optimade_request['representation'] = request.path_info + (('?'+ querystr) if querystr != '' else '')
    optimade_request['relpath'] = request.path_info
    optimade_request['query'] = request.query_params
    if request.method == 'POST':
        optimade_request['postvars'] = request.POST
    else:
        optimade_request['postvars'] = {}
    optimade_request['headers'] = request.META
    
    check_jsonapi_header_requirements(optimade_request['headers'])
    
    return optimade_request
    
@api_view(["GET","POST"])
def base_endpoint(request, version = None):
    optimade_request = _django_request_to_optimade_request(request)
    try:
        output = optimade.process(optimade_request,backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json',json_dumps_params=json_dumps_params)
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code,json_dumps_params=json_dumps_params)

    
@api_view(["GET","POST"])
def base_info(request, version = None):
    optimade_request = _django_request_to_optimade_request(request)
    try:
        output = optimade.process(optimade_request, backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json',json_dumps_params=json_dumps_params)
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code,json_dumps_params=json_dumps_params)

    
@api_view(["GET","POST"])
def base_all(request, id = None, version = None):
    optimade_request = _django_request_to_optimade_request(request)
    try:
        output = optimade.process(optimade_request, backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json',json_dumps_params=json_dumps_params)
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code,json_dumps_params=json_dumps_params)


@api_view(["GET","POST"])
def structures_info(request, version = None):
    optimade_request = _django_request_to_optimade_request(request)
    try:
        output = optimade.process(optimade_request, backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json',json_dumps_params=json_dumps_params)
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code,json_dumps_params=json_dumps_params)

    
@api_view(["GET","POST"])
def structures(request, id = None, version = None):
    optimade_request = _django_request_to_optimade_request(request)
    try:
        output = optimade.process(optimade_request, backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json',json_dumps_params=json_dumps_params)
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code,json_dumps_params=json_dumps_params)


@api_view(["GET","POST"])
def calculations_info(request, version = None):
    optimade_request = _django_request_to_optimade_request(request)
    try:
        output = optimade.process(optimade_request, backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json',json_dumps_params=json_dumps_params)
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code,json_dumps_params=json_dumps_params)
    
    
@api_view(["GET","POST"])
def calculations(request, id = None, version = None):
    optimade_request = _django_request_to_optimade_request(request)
    try:
        output = optimade.process(optimade_request, backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json',json_dumps_params=json_dumps_params)
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code,json_dumps_params=json_dumps_params)



