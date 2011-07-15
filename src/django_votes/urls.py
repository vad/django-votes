from django.conf.urls.defaults import *

from django_votes import views

urlpatterns = patterns('',
    url(r'^vote-down/$', views.down_vote, name='votes_down_vote'),
    url(r'^vote-up/$', views.up_vote, name='votes_up_vote'),
    url(r'^vote-result/(?P<model_name>[^/]+)/(?P<object_id>\d+)/$', views.vote_result, name='votes_vote_result'),
)
