# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from hashlib import md5
from datetime import datetime

from travel_request.apps.request.models import Request, MailConfig, NODE_STATUS

DATETIME_FORMAT = '%Y-%m-%d'
HTML_TEMPLATE = "<html><head><title>%s</title></head><body>%s</body></html>"

def travel_request(request, template_name='request/travel-request.html'):
    """
    display the travel_request form
    """
    if request.method == 'POST':
        form  = request.POST
        host  = request.META.get('HTTP_REFERER', None) or '/'
        title = ""
        body  = ""
        if is_valid(form):
            record = Request()
            record.requestor_email    = form[u'requestor_email']
            record.manager_email      = form[u'manager_email']
            record.departure          = form[u'departure'] 
            record.destination        = form[u'destination'] 
            record.start_date         = form[u'start_date'] 
            record.end_date           = form[u'end_date'] 
            record.working_days       = form[u'working_days']
            record.reason             = form[u'reason']
            record.md5                = md5(''.join(form.values())+str(datetime.now())).hexdigest()

            record.save()             

            send_request(record, host)

            #FIXME maybe need transaction
            title = "Request Success"
            body  = "your request has been sent to %s at %s<p>\
                    Please check feedback at %s"\
                    %(record.manager_email, str(datetime.now()), record.requestor_email)
        else:
            title = "Form Error"
            body  = "Please make sure you've filled in all required fields\
                    and all the fields in a correct form!<p>\
                    Please press <a href=%s>Back</a> and try again!" % host
        
        html = HTML_TEMPLATE % (title, body)
        return HttpResponse(html)

    return render_to_response(template_name,
                              context_instance=RequestContext(request))

def feedback(request, status, feedback_md5):
    """
    manager feedback the request url
    """
    title = ""
    body  = ""
    try:
        q = Request.objects.get(md5=feedback_md5, status='0')
        q.status = status
        q.save()
        title = "Request Feedback"
        body  ="%s at %s %s the request"\
                %(q.manager_email, str(datetime.now()), dict(NODE_STATUS)[int(status)])

        message = "%s\n %s" % (title, body)

        tos = [entry.email for entry in MailConfig.objects.filter(is_cc=False)]
        ccs = [entry.email for entry in MailConfig.objects.filter(is_cc=True)]
        tos.append(q.requestor_email)

        msg = EmailMessage(subject=title,
                           body=message,
                           from_email=q.manager_email,
                           to=tos,
                           cc=ccs,
                           headers={'Cc': ','.join(ccs)})
        msg.send(fail_silently=False)

    except ObjectDoesNotExist:
        update_date = Request.objects.get(md5=feedback_md5).update_date
        title = "Invalid Url"
        body  = "<font style='color:red'>Invalid Url </font>\
                as the Travel Request had been processed at %s" % update_date
    finally:
        html = HTML_TEMPLATE % (title, body)
        return HttpResponse(html)

def is_valid(form):
    """
    verify the form's validation
    """
    for value in form.values():
        if not value:
            return False

    start = datetime.strptime(form[u'start_date'], DATETIME_FORMAT)
    end   = datetime.strptime(form[u'end_date'], DATETIME_FORMAT)
    if start > end:
        return False
    return True

def send_request(record, host):
    feedback_urls = []
    for status, descri in NODE_STATUS:
        feedback_urls.append('<a href="%sfeedback/%s/%s">%s</a> the Requests\n'\
                             %(host, status, record.md5, descri))
       
    message = "Travel Request\n\
            From: %s\n\
            Start: %s To: %s\n\
            Working off days: %s\n\
            Reason: %s\n\n"\
            %(record.requestor_email,
            record.start_date,
            record.end_date,
            record.working_days,
            record.reason) + '\n'.join(feedback_urls)
    
    send_mail('Travel Request',
              message,
              record.requestor_email,
              [record.manager_email],
              fail_silently = False)
