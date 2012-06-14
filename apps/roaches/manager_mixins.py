# -*- coding: utf-8 -*-
from django.db import models

class PublishedMixin(object):
    def published(qs):
        return qs.filter(published=True)

    def unpublished(qs):
        return qs.filter(published=False)


class DeletedMixin(object):
    def deleted(qs):
        return qs.filter(deleted=True)

    def undeleted(qs):
        return qs.filter(deleted=False)

class RoachMixin(object):
    def available(qs):
        return qs.filter(status__status=0, is_banned=False)