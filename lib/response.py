# -*- coding: utf-8 -*-
from __future__ import absolute_import
from functools import wraps
from django.http import HttpResponse
from django.shortcuts import render
from .json import JsonResponse


def json_response(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        result = view(request, *args, **kwargs)
        if isinstance(result, HttpResponse):
            return result
        else:
            return JsonResponse(result)
    return wrapper

def tempate_response(view, template):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        result = view(request, *args, **kwargs)
        if isinstance(result, HttpResponse):
            return result
        else:
            return render(request, template, result)
    return wrapper
