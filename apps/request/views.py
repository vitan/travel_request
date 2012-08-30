# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from hashlib import md5
from datetime import datetime

from travel_request.apps.request.models import Request, NODE_STATUS

def travel_request(request, template_name='request/travel-request.html'):
    """
    display the travel_request form
    """
    if request.method == 'POST':
        form = request.POST
        if is_valid(form):
            record = Request()
            record.requestor    = User.objects.get(email=form[u'requestor_email'])
            record.manager      = User.objects.get(email=form[u'manager_email'])
            record.departure    = form[u'departure'] 
            record.destination  = form[u'destination'] 
            record.start_date   = form[u'start_date'] 
            record.end_date     = form[u'end_date'] 
            record.working_days = form[u'working_days']
            record.reason       = form[u'reason']
            record.md5          = md5(''.join(form.values())+str(datetime.now())).hexdigest()

            record.save()             

            host = request.META.get('HTTP_REFERER', None) or '/'
            send_request(record, host)

            #FIXME maybe need transaction
            success_html = "<html>\
                    <head><title>Request Success</title></head>\
                    <body>The request has been sent to %s at %s<p>\
                    Check feedback at %s</body>\
                    </html>"\
                    %(record.manager.username, str(datetime.now()), record.requestor.email)
            return HttpResponse(success_html)
        else:
            pass

    return render_to_response(template_name,
                              context_instance=RequestContext(request))

def feedback(request, feedback_md5):
    """
    manager feedback the request url
    """
    try:
        q = Request.objects.get(md5=feedback_md5, status='0')
        q.status = '1'
        q.save()
        html = "<html>\
                <head><title>Request Feedback</title></head>\
                <body>%s at %s approved the request</body>\
                </html>"\
                %(q.manager.username, str(datetime.now()))
        return HttpResponse(html)
    except ObjectDoesNotExist:
        raise Http404

def is_valid(form):
    return True

def send_request(record, host):
    message = "Travel Request\n\
              From: %s\n\
              Start: %s To: %s\n\
              Working off days: %s\n\
              Reason: %s\n\
              To Approve the Request by url:%sfeedback/%s"\
              %(record.requestor.username,
                record.start_date,
                record.end_date,
                record.working_days,
                record.reason,
                host, record.md5)
       
    send_mail('Travel Request',
              message,
              record.requestor.email,
              [record.manager.email],
              fail_silently = False)

