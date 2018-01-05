from django.db import models

from account.models import Postgraduate


class Leave(models.Model):
    postgraduate = models.ForeignKey(Postgraduate)
    date = models.DateField()
    excuse = models.TextField()
    state = models.NullBooleanField(null=True)
    time_of_submission = models.DateTimeField()
    time_of_processing = models.DateTimeField(blank=True, null=True)
