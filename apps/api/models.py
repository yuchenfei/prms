from django.db import models

from account.models import Postgraduate


class Device(models.Model):
    postgraduate = models.OneToOneField(Postgraduate)
    imei = models.CharField(max_length=15, blank=True, null=True)
