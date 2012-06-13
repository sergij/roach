# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_exempt
from social_auth.views import complete


admin.autodiscover()
    
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^racing/', include('roaches.urls')),
)

urlpatterns += patterns('',
    url(r'^$', 'roaches.views.index', name='index'),
)

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)
