# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
# from roaches.views import game, create_roach, choose_opponent, create_race, work_for_food, work_abort, train, train_abort, view_stats, evolution
from roaches.views import choose_opponent

urlpatterns = patterns('roaches.views',
    url(r'$', 'game', name='index_game'),
    url(r'^create_roach/$', 'create_roach', name='create_roach'),
    url(r'^compete/(?P<roach_id>\d+)/$', choose_opponent, name='compete'),
    url(r'^create_race/$', 'create_race', name='create_race'),
    url(r'^work/(?P<roach_id>\d+)/$', 'work_for_food', name='work'),
    url(r'^work/abort/(?P<roach_id>\d+)/$', 'work_abort', name='work_abort'),
    url(r'^train/(?P<roach_id>\d+)/$', 'train', name='train'),
    url(r'^train/abort/(?P<roach_id>\d+)/$', 'train_abort', name='train_abort'),
    url(r'^stat/(?P<roach_id>\d+)/$', 'view_stats', name='stat'),
    url(r'^evolution/(?P<roach_id>\d+)/$', 'evolution', name='evolution'),
)
