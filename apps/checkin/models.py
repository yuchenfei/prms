from django.db import models

from account.models import Postgraduate, Teacher


class Computer(models.Model):
    name = models.CharField(max_length=30, unique=True)
    cpu_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class TempCheckInSetting(models.Model):
    teacher = models.ForeignKey(Teacher)
    name = models.CharField(max_length=30)
    date = models.DateField()
    time = models.TimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    computer = models.ForeignKey(Computer, blank=True, null=True)


class TempCheckIn(models.Model):
    target = models.ForeignKey(TempCheckInSetting)
    postgraduate = models.ForeignKey(Postgraduate)
    date_time = models.DateTimeField()


class DailyCheckInSetting(models.Model):
    TIMES_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4')
    )
    teacher = models.ForeignKey(Teacher, unique=True)
    # teacher = models.OneToOneField(Teacher)
    start_date = models.DateField()
    end_date = models.DateField()
    week_option = models.CharField(max_length=7)
    times = models.IntegerField(default=1, choices=TIMES_CHOICES)
    time1_start = models.TimeField()
    time1_end = models.TimeField()
    time2_start = models.TimeField(blank=True, null=True)
    time2_end = models.TimeField(blank=True, null=True)
    time3_start = models.TimeField(blank=True, null=True)
    time3_end = models.TimeField(blank=True, null=True)
    time4_start = models.TimeField(blank=True, null=True)
    time4_end = models.TimeField(blank=True, null=True)
    computer = models.ForeignKey(Computer, blank=True, null=True)


class DailyCheckIn(models.Model):
    postgraduate = models.ForeignKey(Postgraduate)
    date = models.DateField()
    check1 = models.TimeField(blank=True, null=True)
    check2 = models.TimeField(blank=True, null=True)
    check3 = models.TimeField(blank=True, null=True)
    check4 = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.postgraduate.name + self.date.strftime(" %Y-%m-%d")
