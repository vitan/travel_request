# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.mail import send_mail

from travel_request.apps.request.models import Request
from travel_request.apps.request.forms import RequestForm

def travel_request(request, template_name='request/travel-request.html'):
    """
    display the travel_request form
    """
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            requestor_email = form.cleaned_data['requestor_email']
            manager_email = form.cleaned_data['manager_email']
            departure = form.cleaned_data['departure']
            destination = form.cleaned_data['destination']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            working_days = form.cleaned_data['working_days']
            reason = form.cleaned_data['reason']

            record = Request()
            record.requestor   = User.objects.get(email=requestor_email)
            record.manager     = User.objects.get(email=manager_email)
            record.departure   = departure
            record.destination = destination
            record.start_date  = start_date
            record.end_date    = end_date
            record.working_days = working_days
            record.reason = reason
            record.save()

            send_mail('Travel Request',
                      '%s,from %s to %s,working off days %s' %(reason, start_date, end_date, working_days), 
                      requestor_email,
                      [manager_email],
                      fail_silently = False)
        else:
            pass

    else:
        form = RequestForm()

    return render_to_response(template_name, {
        'form': form,
        },context_instance=RequestContext(request))

