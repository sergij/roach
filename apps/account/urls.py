# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from views import login, logout, register, activate, changeemail, password_reset, \
                  password_reset_confirm

urlpatterns = patterns('',
    url(r'^logout/$', logout, {'next_page': '/'}, name='account_logout'),
    url(r'^login/$', login, name='account_login'),

    url(r'^register/$', register, name='account_register'),
    url(r'^activate/$', activate, name='account_activate'),
    url(r'^change-email/$', changeemail, name='account_changeemail'),
    url(r'^reset/$', password_reset, name='account_password_reset'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, name='account_password_reset_confirm'),
)
