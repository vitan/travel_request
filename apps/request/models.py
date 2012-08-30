from django.db import models
from django.contrib.auth.models import User

# Add more options if necessary
STATUS_OPTIONS = ('Processing', 'Approved', 'Postpone', 'Reject', 'Cancelled')
NODE_STATUS = list(enumerate(STATUS_OPTIONS))

class Request(models.Model):
    requestor = models.ForeignKey(User, related_name="requ_requestset")
    manager = models.ForeignKey(User, related_name="mana_requestset")
    #ccs = models.ForeignKey(User)
    departure = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    working_days = models.PositiveIntegerField()
    reason = models.TextField()
    status = models.PositiveSmallIntegerField(default=0, choices=NODE_STATUS)
    md5 = models.CharField(max_length=32) 
