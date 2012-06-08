from django.conf.urls.defaults import *
from main.views import game_main, create_roach, choose_opponent, create_race, work_for_food, work_abort, train, train_abort, view_stats, evolution
urlpatterns = patterns('',
    (r'^$', game_main),
    (r'^create_roach/$', create_roach),
    (r'^compete/(?P<roach_id>\d+)/$', choose_opponent),
    (r'^create_race/$', create_race),
    (r'^work/(?P<roach_id>\d+)/$', work_for_food),
    (r'^work/abort/(?P<roach_id>\d+)/$', work_abort),
    (r'^train/(?P<roach_id>\d+)/$', train),
    (r'^train/abort/(?P<roach_id>\d+)/$', train_abort),
    (r'^stat/(?P<roach_id>\d+)/$', view_stats),
    (r'^evolution/(?P<roach_id>\d+)/$', evolution),
)
