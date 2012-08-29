# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from travel_request.apps.request.models import Request
from travel_request.apps.request.forms import RequestForm

def travel_request(request, template_name='request/travel-request.html'):
    """
    display the travel_request form
    """
    if request.method == 'POST':
        form = RequestForm(request.post)
        if form.is_valid():
            pass
        else:
            pass

    else:
        form = RequestForm()

    return render_to_response(template_name, {
        'form': form,
        },context_instance=RequestContext(request))
