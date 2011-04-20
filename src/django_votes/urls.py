from django.conf.urls.defaults import *
from django_votes.views import down_vote, up_vote

urlpatterns = patterns('',
    url(r'^vote-down/$', down_vote, name='votes_down_vote'),
    url(r'^vote-up/$', up_vote, name='votes_up_vote'),
)
