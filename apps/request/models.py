from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from datetime import datetime

# Add more options if necessary
STATUS_OPTIONS = ('Processing', 'Approved', 'Postponed', 'Rejected', 'Cancelled')
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
