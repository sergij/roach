# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime

class TimestampedMixin(models.Model):
    created_at = models.DateTimeField(_(u'создано'),
                                      auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(_(u'модифицировано'),
                                       auto_now=True, editable=False)

    class Meta:
        abstract = True

class IndexedTimestampedMixin(models.Model):
    created_at = models.DateTimeField(_(u'создано'),
                                      auto_now_add=True, editable=False, db_index=True)
    modified_at = models.DateTimeField(_(u'модифицировано'),
                                       auto_now=True, editable=False, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not kwargs.pop('update_modified', False):
            self.modified_at = datetime.datetime.now()

        super(IndexedTimestampedMixin, self).save(*args, **kwargs)

class TitledMixin(models.Model):
    title = models.CharField(_(u'название'), max_length=255)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


class UpdatebleMixin(models.Model):
    created_at = models.DateTimeField(_(u'создано'), db_index=True,
                                      auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(_(u'модифицировано'), db_index=True,
                                       auto_now=True, editable=False)
    is_deleted = models.BooleanField(_(u'удалено'), default=False, db_index=True)

    def delete(self, using=None):
        assert self._get_pk_val() is not None, "%s object can't be deleted because its %s attribute is set to None." % (self._meta.object_name, self._meta.pk.attname)
        self.is_deleted = True
        if using:
            self.save(using=using)
        else:
            self.save()

    delete.alters_data = True

    class Meta:
        abstract = True

class IndexedTimestampedSkipModifiedMixin(models.Model):
    created_at = models.DateTimeField(_(u'создано'),
                                      auto_now_add=True, editable=False, db_index=True)
    modified_at = models.DateTimeField(_(u'модифицировано'), editable=False, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not kwargs.pop('skip_modified', False):
            self.modified_at = datetime.datetime.now()
        super(IndexedTimestampedSkipModifiedMixin, self).save(*args, **kwargs)