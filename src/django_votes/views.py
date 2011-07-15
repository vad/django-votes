from django.http import (HttpResponseForbidden, HttpResponse,
                         HttpResponseRedirect,)

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django_votes.utils import get_vote_model

def _api_view(func):
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
    if model.objects.filter(object__id=object_id, voter=request.user).count() == 0:
        model.objects.create(object_id=object_id,
                             voter=request.user,
                             value= -1)

    return HttpResponseRedirect(reverse('votes_vote_result', args=[model.get_model_name(),
                                                                   object_id]))

@_api_view
def up_vote(request, model, object_id):
    if model.objects.filter(object__id=object_id, voter=request.user).count() == 0:
        model.objects.create(object_id=object_id,
                             voter=request.user,
                             value=1)

    return HttpResponseRedirect(reverse('votes_vote_result', args=[model.get_model_name(),
                                                                   object_id]))

def vote_result(request, model_name, object_id):
    model = get_vote_model(model_name)

    your_vote = model.objects.filter(voter=request.user)

    if your_vote:
        your_vote = your_vote[0]

    object = model.objects.select_related('object').filter(object__id=object_id)[:1][0].object

    up_votes = model.objects.filter(object__id=object_id,
                                    value__gt=0).count()
    down_votes = model.objects.filter(object__id=object_id,
                                      value__lt=0).count()
    total_votes = model.objects.filter(object__id=object_id).count()

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
