from django.http import (HttpResponseForbidden, HttpResponse,
                         HttpResponseRedirect,)
 
from django.contrib.contenttypes.models import ContentType

from django_votes.utils import get_vote_model

def _api_view(func):
    def view(request):
        if request.method == 'POST':
            # Get comments model
            model_name = request.POST['model']
            ct = ContentType.objects.get(model=model_name)
            model = ct.model_class()     
            object_id = request.POST['object_id']
            instance = model.objects.get(id=object_id)
            # View
            result = func(request, instance)

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
def down_vote(request, instance):    
    instance.down_votes += 1
    instance.save()
    
@_api_view
def up_vote(request, instance):    
    instance.down_votes += 1
    instance.save()
    
    