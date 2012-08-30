from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Add more options if necessary
STATUS_OPTIONS = ('Processing', 'Approved', 'Postpone', 'Reject', 'Cancelled')
NODE_STATUS = list(enumerate(STATUS_OPTIONS))

class Request(models.Model):
    requestor = models.ForeignKey(User, related_name="requ_requestset")
    manager = models.ForeignKey(User, related_name="mana_requestset")
    departure = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    working_days = models.PositiveIntegerField()
    reason = models.TextField()
    status = models.PositiveSmallIntegerField(default=0, choices=NODE_STATUS)
    md5 = models.CharField(max_length=32) 

    def __unicode__(self):
        return "%s requested by %s" % (self.requestor.username,
                                       self.manager.username)

class RequestMailConfig(models.Model):
    user = models.OneToOneField(User)

    request_send = models.ManyToManyField(User, blank=True, related_name="requ_sendset")
    request_cc   = models.ManyToManyField(User, blank=True, related_name="requ_ccset")
    feedback_send= models.ManyToManyField(User, blank=True, related_name="feed_sendset")
    feedback_cc  = models.ManyToManyField(User, blank=True, related_name="feed_ccset")
    
    def __str__(self):
        return "%s's travel-request mail config" % self.user

    def create_mail_config(sender, instance, created, **kwargs):
        if created:
            mail_config, created = RequestMailConfig.objects.get_or_create(user=instance)
    post_save.connect(create_mail_config, sender=User)
