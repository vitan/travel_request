from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from datetime import datetime

# Add more options if necessary
STATUS_OPTIONS = ('Processing', 'Approved', 'Postponed', 'Rejected', 'Cancelled')
NODE_STATUS = list(enumerate(STATUS_OPTIONS))

class Request(models.Model):
    requestor = models.ForeignKey(User, related_name="requ_requestset")
    manager = models.ForeignKey(User, related_name="mana_requestset")
    departure = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    working_days = models.PositiveIntegerField(verbose_name="off working days")
    reason = models.TextField()
    status = models.PositiveSmallIntegerField(default=0, choices=NODE_STATUS)
    md5 = models.CharField(max_length=32) 

    def __unicode__(self):
        return "%s requested by %s" % (self.requestor.username,
                                       self.manager.username)

    def save(self, force_insert=False, force_update=False):
        send_update(self)
        super(Request, self).save(force_insert, force_update)

class RequestMailConfig(models.Model):
    user = models.OneToOneField(User)

    request_send = models.ManyToManyField(User, null=True, blank=True, related_name="requ_sendset")
    request_cc   = models.ManyToManyField(User, null=True, blank=True, related_name="requ_ccset")
    feedback_send= models.ManyToManyField(User, null=True, blank=True, related_name="feed_sendset")
    feedback_cc  = models.ManyToManyField(User, null=True, blank=True, related_name="feed_ccset")
    
    def __unicode__(self):
        return "%s's travel-request mail config" % self.user

    def create_mail_config(sender, instance, created, **kwargs):
        if created:
            mail_config, created = RequestMailConfig.objects.get_or_create(user=instance)
    post_save.connect(create_mail_config, sender=User)

def send_update(record):
    message = "Travel Request has been updated at %s\n\n\
            From: %s\n\
            Start: %s End: %s\n\
            Working off days: %s\n\
            Reason: %s\n\n"\
            %(str(datetime.now()),
              record.requestor.username,
              record.start_date,
              record.end_date,
              record.working_days,
              record.reason)
    
    send_mail('Travel Request Update',
              message,
              "hosted-no-reply@redhat.com",
              [record.requestor.email, record.manager.email],
              fail_silently = False)
