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
from webserver import JsonapiError

class Database(object): 

    def __init__(self):
        pass
        
    def execute(self,sql, parameters={}):
        with connections['default'].cursor() as cursor:
            results = cursor.execute(sql, parameters)
            return [dict([(name[0],d) for name,d in zip(results.description, row)]) for row in results]

    def commit(self):
        return True
            
    def close(self):
        return

backend.initialize(db=Database())

# Create your views here.

@api_view(["GET","POST"])
def base_endpoint(request, version = None):
    optimade_request = {'endpoint':'', 'version':version}
    query = request.query_params 
    try:
        output = optimade.process(reverse('base_endpoint', request=request),optimade_request,query,backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json')
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code)

    
@api_view(["GET","POST"])
def base_info(request, version = None):
    optimade_request = {'endpoint':'info', 'version':version}
    query = request.query_params 
    try:
        output = optimade.process(reverse('base_endpoint', request=request),optimade_request,query,backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json')
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code)

    
@api_view(["GET","POST"])
def base_all(request, id = None, version = None):
    optimade_request = {'endpoint':'all', 'request_id':id, 'version':version}
    query = request.query_params
    try:
        output = optimade.process(reverse('base_endpoint', request=request),optimade_request,query,backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json')
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code)


@api_view(["GET","POST"])
def structures_info(request, version = None):
    optimade_request = {'endpoint':'structures/info', 'version':version}
    query = request.query_params
    try:
        output = optimade.process(reverse('base_endpoint', request=request),optimade_request,query,backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json')
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code)

    
@api_view(["GET","POST"])
def structures(request, id = None, version = None):
    optimade_request = {'endpoint':'structures', 'request_id':id, 'version':version}
    query = request.query_params
    try:
        output = optimade.process(reverse('base_endpoint', request=request),optimade_request,query,backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json')
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code)


@api_view(["GET","POST"])
def calculations_info(request, version = None):
    optimade_request = {'endpoint':'calculations/info', 'version':version}
    query = request.query_params
    try:
        output = optimade.process(reverse('base_endpoint', request=request),optimade_request,query,backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json')
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code)
    
    
@api_view(["GET","POST"])
def calculations(request, id = None, version = None):
    optimade_request = {'endpoint':'all', 'request_id':id, 'version':version}
    query = request.query_params
    try:
        output = optimade.process(reverse('base_endpoint', request=request),optimade_request,query,backend.execute_query, debug=True)
        response = JsonResponse(output, safe=False,content_type='application/vnd.api+json')
        return response
    except optimade.OptimadeError as e:
        error = JsonapiError("Could not process request: "+str(e),e.response_code,e.response_msg)
        return JsonResponse(error.content_json, safe=False,content_type='application/vnd.api+json', status=error.response_code)



