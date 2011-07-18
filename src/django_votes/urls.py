from django.conf.urls.defaults import *

from django_votes import views

urlpatterns = patterns('',
    url(r'^vote-down/$', views.down_vote, name='votes_vote_down'),
    url(r'^vote-up/$', views.up_vote, name='votes_vote_up'),
    url(r'^updownvote-result/(?P<model_name>[^/]+)/(?P<object_id>\d+)/$', views.updownvote_result, name='votes_updownvote_result'),
    url(r'^rating/$', views.rating, name='votes_rating'),
    url(r'^rating-result/(?P<model_name>[^/]+)/(?P<object_id>\d+)/$', views.rating_result, name='votes_rating_result'),
)
