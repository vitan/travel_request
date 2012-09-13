# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from hashlib import md5
from datetime import datetime

from travel_request.apps.request.models import Request, MailConfig

DATETIME_FORMAT = '%Y-%m-%d'
HTML_TEMPLATE = "<html><head><title>%s</title></head><body>%s</body></html>"
ACTION = {'1': 'Approve', '2': 'Postpone', '3': 'Reject'}

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
            record.departure          = form[u'departure'].replace("Others", form[u'departure_Other']) 
            record.destination        = form[u'destination'].replace("Others",form[u'destination_Other'])
            record.start_date         = form[u'start_date'] 
            record.end_date           = form[u'end_date'] 
            record.working_days       = form[u'working_days']
            record.reason             = form[u'reason']
            record.md5                = md5(''.join(form.values())+str(datetime.now())).hexdigest()

            record.save()             

            send_request(record, host)

            title = "Request Success"
            body  = "your request has been sent to %s at %s<p>\
                    Please check feedback at %s"\
                    %(record.manager_email,
                      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      record.requestor_email)
        else:
            title = "Form Error"
            body  = "Please make sure you've filled in all required fields\
                    and all the fields in a correct form!<p>\
                    Please press <a href='javascript:history.go(-1)'>Back</a> and try again!"
        
        html = HTML_TEMPLATE % (title, body)
        return HttpResponse(html)

    return render_to_response(template_name,
                              context_instance=RequestContext(request))

def feedback(request, status, feedback_md5):
    """
    manager feedback the request url
    """
    html_title = ""
    html_body  = ""
    try:
        q = Request.objects.get(md5=feedback_md5, status='0')
        q.status = status
        q.update_date = datetime.now()
        q.save()
        html_title = "Request Feedback"
        html_body  ="%s at %s <font style='color:red'>%s</font> the following request"\
                %(q.manager_email, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ACTION[status])

        email_body = html_body+"<br><br>\
                From: %s<br>\
                Start: %s To: %s<br>\
                Working off days: %s<br>\
                Reason: %s<br><br>"\
                %(q.requestor_email,
                  q.start_date,
                  q.end_date,
                  q.working_days,
                  q.reason)

        #FIXME the manager should be only one? so tos is to
        tos = [entry.email for entry in MailConfig.objects.filter(is_cc=False)]
        ccs = [entry.email for entry in MailConfig.objects.filter(is_cc=True)]
        tos.append(q.requestor_email)

        msg = EmailMultiAlternatives(subject=html_title,
                           from_email="hosted-no-reply@redhat.com",
                           to=tos,
                           cc=ccs,
                           headers={'Cc': ','.join(ccs)})
        
        msg.attach_alternative(email_body, "text/html")
        msg.send(fail_silently=False)

    except ObjectDoesNotExist:
        update_date = Request.objects.get(md5=feedback_md5).update_date
        html_title = "Invalid Url"
        html_body  = "<font style='color:red'>Invalid Url </font>\
                as the Travel Request had been processed at %s" % update_date
    finally:
        html = HTML_TEMPLATE % (html_title, html_body)
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
    for status, descri in ACTION.items():
        feedback_urls.append('<a href="%sfeedback/%s/%s">%s</a>'\
                             %(host, status, record.md5, descri))

    subject = 'Travel Request'
    body = "Travel Request<br>\
            From: %s<br>\
            Start: %s To: %s<br>\
            Working off days: %s<br>\
            Reason: %s<br><br>\
            Manager will receive another email to feedback the request<br>"\
            %(record.requestor_email,
            record.start_date,
            record.end_date,
            record.working_days,
            record.reason)
    feedback = '<br>'.join(feedback_urls)
    tos = [entry.email for entry in MailConfig.objects.filter(is_cc=False)]
    ccs = [entry.email for entry in MailConfig.objects.filter(is_cc=True)]

    msg = EmailMultiAlternatives(subject=subject,
                                 from_email=record.requestor_email,
                                 to = tos)
    msg.attach_alternative(body+feedback, "text/html")
    msg.send(fail_silently=False)

    tos.append(record.manager_email)
    msg = EmailMultiAlternatives(subject=subject,
                                 from_email=record.requestor_email,
                                 to = tos,
                                 cc = ccs,
                                 headers={'Cc': ','.join(ccs)})
    msg.attach_alternative(body, "text/html")
    msg.send(fail_silently=False)
