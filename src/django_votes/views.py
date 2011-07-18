from django.http import (HttpResponseForbidden, HttpResponse,
                         HttpResponseRedirect,)

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.models import Avg

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django_votes.utils import get_vote_model

def _api_view(func):
    """
    Extracts model information from the POST dictionary and gets the vote model from them.
    """

    def view(request):
        if request.method == 'POST':
            # Get comments model
            model_name = request.POST['model']
            model = get_vote_model(model_name)

            object_id = request.POST['object_id']
            # View
            result = func(request, model, object_id)

            if result:
                return result
            else:
                # ... and redirect to next.
                if 'next' in request.REQUEST:
                    return HttpResponseRedirect(request.REQUEST['next'])
                else:
                    return HttpResponse('OK')
        else:
            # Default response: 403
            return HttpResponseForbidden()
    return view

@_api_view
def down_vote(request, model, object_id):
    """
    Dislikes an item
    """

    if model.objects.filter(object__id=object_id, voter=request.user).count() == 0:
        model.objects.create(object_id=object_id,
                             voter=request.user,
                             value= -1)

    return HttpResponseRedirect(reverse('votes_updownvote_result', args=[model.get_model_name(),
                                                                         object_id]))

@_api_view
def up_vote(request, model, object_id):
    """
    Likes an item
    """

    if model.objects.filter(object__id=object_id, voter=request.user).count() == 0:
        model.objects.create(object_id=object_id,
                             voter=request.user,
                             value=1)

    return HttpResponseRedirect(reverse('votes_updownvote_result', args=[model.get_model_name(),
                                                                         object_id]))

@_api_view
def rating(request, model, object_id):
    """
    Gives a rating to an item
    """

    rating = request.POST['rating']

    if model.objects.filter(object__id=object_id, voter=request.user).count() == 0:
        model.objects.create(object_id=object_id,
                             voter=request.user,
                             value=rating)

    return HttpResponseRedirect(reverse('votes_rating_result', args=[model.get_model_name(),
                                                                     object_id]))

def updownvote_result(request, model_name, object_id):
    """
    Display the likes and dislikes of an item
    """

    model = get_vote_model(model_name)

    # Get your own vote
    your_vote = model.objects.filter(voter=request.user)

    if your_vote:
        your_vote = your_vote[0]

    # Extract the object what these votes are about. (There's gotta be a better way to do this)
    object = model.objects.select_related('object').filter(object__id=object_id)[:1][0].object

    # Get the likes
    up_votes = model.objects.filter(object__id=object_id,
                                    value__gt=0).count()
    # Get the dislikes
    down_votes = model.objects.filter(object__id=object_id,
                                      value__lt=0).count()
    # Get the total votes
    total_votes = model.objects.filter(object__id=object_id).count()

    # Calculate the percentages in order to fill the bars
    up_pct = (float(up_votes) / float(total_votes) if total_votes else 0) * 98
    down_pct = (float(down_votes) / float(total_votes) if total_votes else 0) * 98

    context = {'model_name': model_name,
               'object': object,
               'up_votes': up_votes,
               'down_votes': down_votes,
               'your_vote': your_vote,
               'total_votes': total_votes,
               'up_pct': up_pct,
               'down_pct': down_pct}

    return render_to_response('django_votes/updownvote.html',
                              context,
                              context_instance=RequestContext(request))

def rating_result(request, model_name, object_id):
    """
    Display the average rating of an item
    """

    model = get_vote_model(model_name)

    # Get your own vote
    your_vote = model.objects.filter(voter=request.user)

    if your_vote:
        your_vote = your_vote[0]

    # Extract the object what these votes are about. (There's gotta be a better way to do this)
    object = model.objects.select_related('object').filter(object__id=object_id)[:1][0].object

    # Get the average rating
    rating = model.objects.filter(object__id=object_id).aggregate(value=Avg('value'))

    context = {'model_name': model_name,
               'object': object,
               'rating': rating['value'],
               'your_vote': your_vote}

    return render_to_response('django_votes/rating.html',
                              context,
                              context_instance=RequestContext(request))
