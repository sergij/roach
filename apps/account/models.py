# -*- coding: utf-8 -*-
import random
from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.hashcompat import sha_constructor
from django.core.exceptions import ObjectDoesNotExist


DEFAULT_REQUEST_MAX_AGE = 1 * 3600 # sec


class ChangeEmailRequestManager(models.Manager):
    def create_request(self, user, email):
        try:
            while True:
                validation_key = sha_constructor(str(random.random()) + \
                                                 str(datetime.now())).hexdigest()
                self.get(validation_key=validation_key)

        except ObjectDoesNotExist:
            # запрос с таким же validation_key не найден, и это хорошо
            pass

        try:
            req = self.get(user=user)
        except ObjectDoesNotExist:
            req = self.model(user=user)

        req.email = email
        req.validation_key = validation_key
        req.expired_at = datetime.now() + timedelta(0, DEFAULT_REQUEST_MAX_AGE)
        req.save()

        return req

    def delete_expired_requests(self):
        self.filter(expired_at__lt=datetime.now()).delete()


class ChangeEmailRequest(models.Model):
    user = models.OneToOneField(User, related_name='new_email_info')
    email = models.EmailField(_(u'адрес электронной почты'), max_length=75)
    validation_key = models.CharField(_('проверочный код'), max_length=40,
                                      unique=True)
    expired_at = models.DateTimeField(_('истекает в'))

    objects = ChangeEmailRequestManager()

    @property
    def is_expired(self):
        return self.expired_at < datetime.now()

