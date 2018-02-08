from django.db import models

from account.models import Postgraduate, Teacher


class Computer(models.Model):
    name = models.CharField(max_length=30, unique=True)
    cpu_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class CheckInSetting(models.Model):
    TYPE_CHOICES = (
        (1, 'Daily Check In'),
        (2, 'Meeting Check In'),
    )
    teacher = models.ForeignKey(Teacher)
    c_type = models.IntegerField(choices=TYPE_CHOICES)
    enable = models.BooleanField(default=False)
    date_time = models.DateTimeField()
    computer = models.ForeignKey(Computer, blank=True, null=True)


class DailyCheckIn(models.Model):
    postgraduate = models.ForeignKey(Postgraduate)
    date = models.DateField()
    forenoon_in = models.TimeField(blank=True, null=True)
    forenoon_out = models.TimeField(blank=True, null=True)
    afternoon_in = models.TimeField(blank=True, null=True)
    afternoon_out = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.postgraduate.name + self.date.strftime(" %Y-%m-%d")


class MeetingCheckIn(models.Model):
    target = models.ForeignKey(CheckInSetting)
    postgraduate = models.ForeignKey(Postgraduate)
    date_time = models.DateTimeField()
