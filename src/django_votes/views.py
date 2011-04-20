from django.http import (HttpResponseForbidden, HttpResponse,
                         HttpResponseRedirect,)
 
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

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
                             value=-1)
    
@_api_view
def up_vote(request, model, object_id):    
    if model.objects.filter(object__id=object_id, voter=request.user).count() == 0:
        model.objects.create(object_id=object_id, 
                             voter=request.user,
                             value=1)
    
    