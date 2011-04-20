from django.http import (HttpResponseForbidden, HttpResponse,
                         HttpResponseRedirect,)
 
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

def _api_view(func):
    def view(request):
        if request.method == 'POST':
            # Get comments model
            model_name = request.POST['model']      
            app = model_name.split('.')[0]
            model = model_name.split('.')[1]    
            ct = ContentType.objects.get(model=model, app_label=app)
            model = ct.model_class()     
            object_id = request.POST['object_id']
            instance = model.objects.get(id=object_id)
            # View
            result = func(request, instance, user)

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
    instances.votes    
    instance.down_votes += 1
    instance.save()
    
@_api_view
def up_vote(request, instance):    
    instance.up_votes += 1
    instance.save()
    
    