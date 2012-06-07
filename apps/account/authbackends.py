# -*- coding: utf-8 -*-
from django.db import connection
from django.contrib.auth.models import User, Permission
from django.contrib.auth.backends import ModelBackend as DjModelBackend
from django.db.models import Q

class ModelBackend(DjModelBackend):
    supports_object_permissions = False
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(Q(username__iexact=username)|Q(email__iexact=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
