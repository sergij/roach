from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()
import settings
from views import home_page, delete_races
urlpatterns = patterns('',
    # (r'^roach/', include('roach.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^$', home_page),
    (r'^delete_race/$', delete_races),
    (r'^accounts/', include('roach.register.urls')),
    (r'^game/', include('roach.main.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT}),
)
