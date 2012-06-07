# coding: utf-8
from __future__ import absolute_import

import os
import uuid
import datetime
import hashlib
from itertools import chain, repeat, islice, takewhile, imap, starmap
from django.template import loader, RequestContext
from django.contrib.auth.models import User
from django.conf import settings

from .json import JsonResponse

def force_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return force_int(default)

def amplify(it, to, with_=None):
    """Дополняет список (итератор) до заданного кол-ва значений

     >>> amplify([1, 2, 3], 5, 0)
    [1, 2, 3, 0, 0]
    >>> amplify([1, 2, 3], 2, 0)
    [1, 2]
    >>> amplify([1, 2, 3], 5)
    [1, 2, 3, None, None]
    >>> amplify(['name', 'surname'], 3, '')
    ['name', 'surname', '']
    """
    return list(islice(chain(iter(it), repeat(with_)), to))


def is_dict_path_exists(target_dict, tested_path=()):
    """Проверяет существование вложенных элементов словаря

    >>> is_dict_path_exists({'a': {'b': {'c': ''}}}, ('a', 'b'))
    True
    >>> is_dict_path_exists({'a': {'b': {'c': ''}}}, ('a', 'b', 'c'))
    True
    >>> is_dict_path_exists({'a': {'b': {'c': ''}}}, ('a', 'b', 'x'))
    False
    >>> is_dict_path_exists({'a': {'b': {'c': ''}}}, ('a', 'b', 'c', 'd'))
    False

    """
    td = target_dict
    try:
        for p in tested_path:
            if not isinstance(td, dict):
                return False
            td = td[p]
        return True
    except KeyError:
        return False

def takeby(n, it):
    """Выбирает по 'n' элементов из итератора it"""
    return takewhile(bool, imap(list, starmap(islice, repeat((iter(it), n)))))


# from http://code.djangoproject.com/ticket/2659
def get_object_or_none(klass, *args, **kwargs):
    try:
        return klass._default_manager.get(*args, **kwargs)
    except klass.DoesNotExist:
        return None

# http://jquery.malsup.com/form/#file-upload
# нужен для возвращения json результата, если в ajax-форме был сабмит файлов
# json отдаётся в text/plain
class AjaxIFrameJsonResponse(JsonResponse):
    def __init__(self, request, data):
        self.for_iframe = not request.is_ajax()

        if self.for_iframe:
            super(AjaxIFrameJsonResponse, self).__init__(data, mimetype='text/plain; charset=utf-8')
        else:
            super(AjaxIFrameJsonResponse, self).__init__(data)


class AjaxFormResponse(AjaxIFrameJsonResponse):
    def __init__(self, request, **kwargs):
        super(AjaxFormResponse, self).__init__(request, kwargs)


class SuccessAjaxFormResponse(AjaxFormResponse):
    def __init__(self, request, type, data, **kwargs):
        super(SuccessAjaxFormResponse, self).__init__(request, success=True,
                                                      type=type, data=data,
                                                      **kwargs)

class ErrorAjaxFormResponse(AjaxIFrameJsonResponse):
    def __init__(self, request, **kwargs):
        super(ErrorAjaxFormResponse, self).__init__(request, success=False,
                                                    **kwargs)

def render_template(request, template_name, context):
    """Рендерит указанный шаблон с RequestContext, возвращает строку"""
    c = RequestContext(request, context)
    t = loader.get_template(template_name)
    return t.render(c)


def only_int_list(it):
    """Возвращает приводимые к int элементы начального списка"""
    res_list = []
    for i in iter(it):
        try:
            res_list.append(int(i))
        except ValueError:
            continue
    return res_list

def uniquify(seq):
    """Уникализирует список"""
    def uniquify_generator(seq):
        seen = set()
        for item in seq:
            if item in seen:
                continue
            seen.add(item)
            yield item
    return list(uniquify_generator(seq))


def user_list_hiring(obj_list, field_name):
    related = User._meta.get_field_by_name(field_name)[0]
    field_cache_name = related.get_cache_name()

    rel_model = related.field.model
    rel_field_name = related.field.name

    key_name = related.field.rel.field_name

    key_list = obj_list.keys()

    filter_spec = {rel_field_name + '__' + key_name +'__in': key_list}

    rel_obj_list = rel_model._base_manager.filter(**filter_spec)

    rel_obj_dict = dict((getattr(ro, related.field.attname), ro) for ro in rel_obj_list)

    for ids in key_list:
        setattr(obj_list[ids], field_cache_name, rel_obj_dict.get(ids))
    return ''

def translit_ru2en(words):
    words = words.lower().split()
    translit_alpha = {u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd', u'е': u'e', u'ё': u'e', u'ж': u'zh', u'з': u'z', u'и': u'i', u'й': u'j', u'к': u'k',  u'л': u'l',  u'м': u'm',\
                  u'н': u'n', u'о': u'o',  u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f', u'х': u'h', u'ц': u'c', u'ч': u'ch', u'ш': u'sh', u'щ': u'sch', u'ъ': u'',\
                  u'ы': u'i', u'ь': '', u'э': u'e', u'ю': u'yu', u'я': u'ya'}
    result = []
    for word in words:
        result_word = ""
        for alpha in word:
            try:
                result_word += translit_alpha[alpha]
            except KeyError:
                result_word += alpha
        result.append(result_word)
    return ' '.join(result)

def translit_other_maps(words):
    words = words.lower().split()
    translit_maps = [{u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd', u'е': u'e', u'ё': u'e', u'ж': u'zh', u'з': u'z', u'и': u'i', u'й': u'j', u'к': u'k',  u'л': u'l',  u'м': u'm',\
                  u'н': u'n', u'о': u'o',  u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f', u'х': u'h', u'ц': u'c', u'ч': u'ch', u'ш': u'sh', u'щ': u'sch', u'ъ': u'',\
                  u'ы': u'i', u'ь': '', u'э': u'e', u'ю': u'yu', u'я': u'ya'},\
                    {u'а': u'a', u'б': u'b', u'в': u'w', u'г': u'g', u'д': u'd', u'е': u'e', u'ё': u'e', u'ж': u'j', u'з': u'z', u'и': u'i', u'й': u'y', u'к': u'k',  u'л': u'l',  u'м': u'm',\
                  u'н': u'n', u'о': u'o',  u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'y', u'ф': u'ph', u'х': u'h', u'ц': u'c', u'ч': u'ch', u'ш': u'sh', u'щ': u'sch', u'ъ': u'',\
                  u'ы': u'i', u'ь': '', u'э': u'e', u'ю': u'iu', u'я': u'ia'},\
                    {u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd', u'е': u'e', u'ё': u'e', u'ж': u'g', u'з': u'z', u'и': u'i', u'й': u'y', u'к': u'k',  u'л': u'l',  u'м': u'm',\
                  u'н': u'n', u'о': u'o',  u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'y', u'ф': u'ph', u'х': u'kh', u'ц': u'c', u'ч': u'ch', u'ш': u'sh', u'щ': u'sh', u'ъ': u'',\
                  u'ы': u'y', u'ь': '', u'э': u'e', u'ю': u'ju', u'я': u'ja'}]

    result = []
    # diff = [{ u'ю': [u'ju', u'yu', u'iu', u'u']}, {u'я': [u'ja', u'ya', u'ia']}, {u'х': [u'h', u'kh']}, {u'ф':[u'f', u'ph']}, {u'щ': [u'sh', u'sch']}]

    for trans_map in translit_maps:
        for word in words:
            result_word = ""
            for alpha in word:
                try:
                    result_word += trans_map[alpha]
                except KeyError:
                    result_word += alpha
            if result_word not in result:
                result.append(result_word)
    return ' '.join(result)


def get_uuid_name_generator(prefix=''):
    return lambda instance, filename: uuid_name_generator(filename, prefix=prefix)

def uuid_name_generator(filename, prefix=''):
    ext = os.path.splitext(filename)[1]
    name = uuid.uuid4().hex + ext
    path = u'/'.join(filter(None, (prefix, name[:2], name[2:4], name)))
    return path

import re
def handle_temp_image(uploaded_file):
    """Save uploaded file to temp dir with new generated name"""
    """Сохраняет загруженный файл во временной директории с новым сгенерированным именем"""

    media_root = settings.MEDIA_ROOT
    while True:
        fn = uuid_name_generator(uploaded_file.name, prefix='tmp')
        file_path = os.path.join(media_root, fn)
        if not os.path.exists(file_path):
            break
    try:
        os.makedirs(os.path.dirname(file_path))
    except OSError:
        pass
    f = file(file_path, 'wb')
    for chunk in uploaded_file.chunks():
        f.write(chunk)
    f.close()
    return fn

def mat_detector(phrase):
    censure_pattern = u"\w{0,5}[хx]([хx\s\!@#\$%\^&*+-\|\/]{0,6})[уy]([уy\s\!@#\$%\^&*+-\|\/]{0,6})[ёiлeеюийя]\w{0,7}|\w{0,6}[пp]([пp\s\!@#\$%\^&*+-\|\/]{0,6})[iие]([iие\s\!@#\$%\^&*+-\|\/]{0,6})[3зс]([3зс\s\!@#\$%\^&*+-\|\/]{0,6})[дd]\w{0,10}|[сcs][уy]([уy\!@#\$%\^&*+-\|\/]{0,6})[4чkк]\w{1,3}|\w{0,4}[bб]([bб\s\!@#\$%\^&*+-\|\/]{0,6})[lл]([lл\s\!@#\$%\^&*+-\|\/]{0,6})[yя]\w{0,10}|\w{0,8}[её][bб][лске@eыиаa][наи@йвл]\w{0,8}|\w{0,4}[еe]([еe\s\!@#\$%\^&*+-\|\/]{0,6})[бb]([бb\s\!@#\$%\^&*+-\|\/]{0,6})[uу]([uу\s\!@#\$%\^&*+-\|\/]{0,6})[н4ч]\w{0,4}|\w{0,4}[еeё]([еeё\s\!@#\$%\^&*+-\|\/]{0,6})[бb]([бb\s\!@#\$%\^&*+-\|\/]{0,6})[нn]([нn\s\!@#\$%\^&*+-\|\/]{0,6})[уy]\w{0,4}|\w{0,4}[еe]([еe\s\!@#\$%\^&*+-\|\/]{0,6})[бb]([бb\s\!@#\$%\^&*+-\|\/]{0,6})[оoаa@]([оoаa@\s\!@#\$%\^&*+-\|\/]{0,6})[тnнt]\w{0,4}|\w{0,10}[ё]([ё\!@#\$%\^&*+-\|\/]{0,6})[б]\w{0,6}|\w{0,4}[pп]([pп\s\!@#\$%\^&*+-\|\/]{0,6})[иeеi]([иeеi\s\!@#\$%\^&*+-\|\/]{0,6})[дd]([дd\s\!@#\$%\^&*+-\|\/]{0,6})[oоаa@еeиi]([oоаa@еeиi\s\!@#\$%\^&*+-\|\/]{0,6})[рr]\w{0,12}"
    return bool(re.search(censure_pattern, phrase.lower(), re.I|re.M))


def ranking_array(vector):
    return sorted(range(len(vector)), key=vector.__getitem__, reverse=True)

def rankdata(a):
    length = len(a)
    ivec = ranking_array(a)
    svec = [a[rank] for rank in ivec]
    sumranks = 0
    dupcount = 0
    rank_array = [0] * length
    for i in xrange(length):
        sumranks += i
        dupcount += 1
        if i == length - 1 or svec[i] != svec[i + 1]:
            averank = sumranks / float(dupcount) + 1
            for j in xrange(i - dupcount + 1, i + 1):
                rank_array[ivec[j]] = averank
            sumranks = 0
            dupcount = 0
    return rank_array

def hash_maker(remote_addr):
    return hashlib.sha256(remote_addr + str(datetime.datetime.now())).hexdigest()