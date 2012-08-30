# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.mail import send_mail
from hashlib import md5
from datetime import datetime

from travel_request.apps.request.models import Request

def travel_request(request, template_name='request/travel-request.html'):
    """
    display the travel_request form
    """
    if request.method == 'POST':
        form = request.POST
        if 1 == 1:
            record = Request()
            record.requestor    = User.objects.get(email=form[u'requestor_email'])
            record.manager      = User.objects.get(email=form[u'manager_email'])
            record.departure    = form[u'departure'] 
            record.destination  = form[u'destination'] 
            record.start_date   = form[u'start_date'] 
            record.end_date     = form[u'end_date'] 
            record.working_days = form[u'working_days']
            record.reason       = form[u'reason']
            record.md5          = md5(form[u'requestor_email']+
                                      form[u'manager_email']+
                                      form[u'departure']+ 
                                      form[u'destination']+
                                      form[u'start_date']+ 
                                      form[u'end_date']+ 
                                      form[u'working_days']+
                                      form[u'reason']+
                                      str(datetime.now())).hexdigest()

            record.save()             
            message = 'because %s,from %s to %s,working off days %s\n127.0.0.1:8000/travel_request/feedback/'+record.md5
            send_mail('Travel Request',
                      message %(form['reason'], form['start_date'], form['end_date'], form['working_days']), 
                      form['requestor_email'],
                      [form['manager_email']],
                      fail_silently = False)
        else:
            pass

    return render_to_response(template_name, context_instance=RequestContext(request))

def feedback(request, feedback_md5):
    """
    manager feedback the request url
    """
    now = datetime.now()
    q = Request.objects.get(md5=feedback_md5)
    q.status = '1'
    q.save()
    html = "<html><head><title>Request Feedback</title></head><body>%s at %s approved the request"% (q.manager.username, str(now))

    return HttpResponse(html)
