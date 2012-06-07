# -*- coding: utf-8 -*-
from django.http import HttpResponseBadRequest
from functools import wraps

def ajax_required(func):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return func(request, *args, **kwargs)
    return wrapper
