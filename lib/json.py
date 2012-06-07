# coding: utf-8
from decimal import Decimal
from functools import wraps

from django.http import HttpResponse
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.db import models
from django.utils.functional import Promise
from django.utils.encoding import force_unicode
from django.utils import simplejson as json



def model_to_dict(instance, fields=None, exclude=None):
    # avoid a circular import
    from django.db.models.fields.related import ManyToManyField
    opts = instance._meta
    data = {}
    for f in opts.fields + opts.many_to_many:
        if fields and not f.name in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if isinstance(f, ManyToManyField):
            # If the object doesn't have a primry key yet, just use an empty
            # list for its m2m fields. Calling f.value_from_object will raise
            # an exception.
            if instance.pk is None:
                data[f.name] = []
            else:
                # MultipleChoiceWidget needs a list of pks, not object instances.
                data[f.name] = [obj.pk for obj in f.value_from_object(instance)]
        else:
            data[f.name] = f.value_from_object(instance)
    return data

def json_encode(data):
    """
    The main issues with django's default json serializer is that properties that
    had been added to an object dynamically are being ignored (and it also has
    problems with some models).
    """

    def _any(data):
        ret = None
        # Opps, we used to check if it is of type list, but that fails
        # i.e. in the case of django.newforms.utils.ErrorList, which extends
        # the type "list". Oh man, that was a dumb mistake!
        if isinstance(data, list):
            ret = _list(data)
        # Same as for lists above.
        elif isinstance(data, dict):
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, models.Model):
            dict_data = model_to_dict(data)
            ret = _dict(dict_data)
#                ret = _model(data)
        # here we need to encode the string as unicode (otherwise we get utf-16 in the json-response)
        elif isinstance(data, basestring):
            ret = unicode(data)
        # see http://code.djangoproject.com/ticket/5868
        elif isinstance(data, Promise):
            ret = force_unicode(data)
        else:
            ret = data
        return ret

    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))
        # And additionally encode arbitrary properties that had been added.
        fields = dir(data.__class__) + ret.keys()
        add_ons = [k for k in dir(data) if k not in fields]
        for k in add_ons:
            ret[k] = _any(getattr(data, k))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k,v in data.items():
            ret[k] = _any(v)
        return ret

    ret = _any(data)

    return json.dumps(ret, ensure_ascii=False, cls=DateTimeAwareJSONEncoder)


class JsonResponse(HttpResponse):
    """Возвращает HttpResponse с json mimetype'ом"""
    def __init__(self, data, mimetype="application/json", **kwarg):
        json_data = self.json_dumps(data)
        super(JsonResponse, self).__init__(json_data, mimetype=mimetype, **kwarg)

    def json_dumps(self, data):
        return json_encode(data)

# JSONP
class JsonpResponse(HttpResponse):
    def __init__(self, data, callback, mimetype="text/javascript", **kwarg):
        json_data = self.json_dumps(data)
        jsonp = "%s(%s)" % (callback, json_data)
        super(JsonpResponse, self).__init__(jsonp, mimetype=mimetype, **kwarg)

    def json_dumps(self, data):
        return json_encode(data)


def jsonp(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)

        # если результат не json, он не сможет стать jsonp
        if 'application/json' not in response['Content-Type']:
            return response

        # определяем наличие указание коллбека
        callback = request.GET.get('callback')
        if not callback:
            callback = request.GET.get('jsonp')
        # нет коллбека -- не jsonp
        if not callback:
            return response

        response['Content-Type'] = 'text/javascript; charset=utf-8'
        response.content = '%s(%s)' % (callback, response.content)
        return response

    return wrapper
