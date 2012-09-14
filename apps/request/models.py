from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.core.mail import EmailMultiAlternatives

# Add more options if necessary
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
STATUS_OPTIONS = ('Processing', 'Approved', 'Postponed', 'Rejected')
ACTION = {'1': 'Approve', '2': 'Postpone', '3': 'Reject'}
NODE_STATUS = list(enumerate(STATUS_OPTIONS))

class Request(models.Model):
    requestor_email = models.EmailField(max_length=255, null=True, blank=True)
    manager_email   = models.EmailField(max_length=255, null=True, blank=True)
    departure       = models.CharField(max_length=1024)
    destination     = models.CharField(max_length=1024)
    start_date      = models.DateTimeField()
    end_date        = models.DateTimeField()
    working_days    = models.PositiveIntegerField(verbose_name="off working days")
    reason          = models.TextField()
    status          = models.PositiveSmallIntegerField(default=0, choices=NODE_STATUS)
    md5             = models.CharField(max_length=32) 
    update_date     = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s requested by %s" % (self.requestor_email,
                                       self.manager_email)

class MailConfig(models.Model):
    username     = models.CharField(max_length=255, null=True, blank=True)
    email        = models.EmailField(max_length=255)
    is_cc        = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s" % self.username

@receiver(post_save, sender=Request)
def feedback_handler(sender, **kwargs):
    obj = kwargs['instance']
    if obj.status is not 0:
        subject = "Request Feedback"
        feedback  ="%s at %s <font style='color:red'>%s</font> the following request"\
                %(obj.manager_email,
                  obj.update_date.strftime(DATETIME_FORMAT),
                  ACTION[str(obj.status)])

        email_body = feedback+"<br><br>\
                From: %s<br>\
                Departure: %s<br>\
                Destination: %s<br>\
                Start: %s To: %s<br>\
                Working off days: %s<br>\
                Reason: %s<br><br>"\
                %(obj.requestor_email,
                  obj.departure,
                  obj.destination,
                  obj.start_date,
                  obj.end_date,
                  obj.working_days,
                  obj.reason)

        #FIXME the manager should be only one? so tos is to
        tos = [entry.email for entry in MailConfig.objects.filter(is_cc=False)]
        ccs = [entry.email for entry in MailConfig.objects.filter(is_cc=True)]
        tos.append(obj.requestor_email)

        msg = EmailMultiAlternatives(subject=subject,
                                     from_email="hosted-no-reply@redhat.com",
                                     to=tos,
                                     cc=ccs,
                                     headers={'Cc': ','.join(ccs)})
        
        msg.attach_alternative(email_body, "text/html")
        msg.send(fail_silently=False)
    else:
        pass
