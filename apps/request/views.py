# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from hashlib import md5
from datetime import datetime

from apps.request.models import Team, Request, MailConfig, ACTION, DATETIME_FORMAT

HTML_TEMPLATE = "<html><head><title>%s</title></head><body>%s</body></html>"

def travel_request(request, template_name='request/travel-request.html'):
    """
    display the travel_request form
    """
    if request.method == 'POST':
        form  = request.POST
        title = ""
        body  = ""
        if is_valid(form):
            record = Request()
            record.requestor_email    = form[u'requestor_email']
            record.team               = Team.objects.get(name = form[u'team'])
            record.departure          = form[u'departure'].replace("Others", form[u'departure_Other']) 
            record.destination        = form[u'destination'].replace("Others",form[u'destination_Other'])
            record.start_date         = form[u'start_date'] 
            record.end_date           = form[u'end_date'] 
            record.working_days       = form[u'working_days']
            record.reason             = form[u'reason']
            record.md5                = md5(''.join(form.values())+str(datetime.now())).hexdigest()

            record.save()             

            send_request(record, settings.HOSTNAME)

            title = "Request Success"
            body  = "your request has been sent to %s at %s<p>\
                    Please check feedback at %s"\
                    %(record.team.functional_manager_email,
                      datetime.now().strftime(DATETIME_FORMAT),
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
                %(q.team.functional_manager_email, q.update_date.strftime(DATETIME_FORMAT), ACTION[status])
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
    if not all(form.values()):
        return False

    try:
        start = datetime.strptime(form[u'start_date'], DATETIME_FORMAT[:8])
        end   = datetime.strptime(form[u'end_date'], DATETIME_FORMAT[:8])
    except ValueError:
        return False
    if start > end:
        return False
    return True

def send_request(record, host):
    feedback_urls = []
    for status, descri in ACTION.items():
        feedback_urls.append('<a href="%sfeedback/%s/%s">%s</a>'\
                             %(host, status, record.md5, descri))

    subject = 'Travel Request'
    base_body = "Travel Request<br>\
            From: %s<br>\
            Departure: %s<br>\
            Destination: %s<br>\
            Start: %s To: %s<br>\
            Working off days: %s<br>\
            Reason: %s<br><br>"\
            %(record.requestor_email,
              record.departure,
              record.destination,
              record.start_date,
              record.end_date,
              record.working_days,
              record.reason)

    tos = [entry.email for entry in MailConfig.objects.filter(is_cc=False)]
    ccs = [entry.email for entry in MailConfig.objects.filter(is_cc=True)]
    feedback = '<br>Once you click the following url:<br>' +\
            '<br>'.join(feedback_urls) +\
            '<br> the feedback will be Sent to:<br>'+\
            record.requestor_email + '<br>' + record.team.functional_manager_email +\
            '<br> CC to: <br>'+\
            '<br>'.join(set(ccs))

    msg = EmailMultiAlternatives(subject=subject,
                                 from_email="hosted-no-reply@redhat.com",
                                 to = set(tos))
    msg.attach_alternative(base_body+feedback, "text/html")
    msg.send(fail_silently=False)

    tos.append(record.team.functional_manager_email)
    msg = EmailMultiAlternatives(subject=subject,
                                 from_email=record.requestor_email,
                                 to = set(tos),
                                 cc = set(ccs),)
    msg.attach_alternative(base_body, "text/html")
    msg.send(fail_silently=False)
