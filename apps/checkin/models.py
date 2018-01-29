from django.db import models

from account.models import Postgraduate


class CheckIn(models.Model):
    postgraduate = models.ForeignKey(Postgraduate)
    date = models.DateField()
    forenoon_in = models.TimeField(blank=True, null=True)
    forenoon_out = models.TimeField(blank=True, null=True)
    afternoon_in = models.TimeField(blank=True, null=True)
    afternoon_out = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.postgraduate.name + self.date.strftime(" %Y-%m-%d")


class Computer(models.Model):
    name = models.CharField(max_length=30, unique=True)
    cpu_id = models.CharField(max_length=20, unique=True)
