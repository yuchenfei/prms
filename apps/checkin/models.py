from django.db import models

from account.models import Postgraduate, Teacher


class Computer(models.Model):
    teacher = models.ForeignKey(Teacher)
    name = models.CharField(max_length=30)
    cpu_id = models.CharField(max_length=20)

    class Meta:
        unique_together = ('teacher', 'name')

    def __str__(self):
        return self.name


class TempCheckInSetting(models.Model):
    teacher = models.ForeignKey(Teacher)
    name = models.CharField(max_length=30)
    date = models.DateField()
    time = models.TimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_group = models.BooleanField(default=False)
    computer = models.ManyToManyField(Computer)


class TempCheckIn(models.Model):
    target = models.ForeignKey(TempCheckInSetting)
    postgraduate = models.ForeignKey(Postgraduate)
    date_time = models.DateTimeField()


class DailyCheckInSetting(models.Model):
    TIMES_CHOICES = (
        (1, '单次签到'),
        (2, '一个时间段'),
        (4, '两个时间段')
    )
    teacher = models.OneToOneField(Teacher)
    start_date = models.DateField()
    end_date = models.DateField()
    week_option = models.CharField(max_length=7)
    times = models.IntegerField(default=1, choices=TIMES_CHOICES)
    time1_start = models.TimeField(blank=True, null=True)
    time1_end = models.TimeField(blank=True, null=True)
    time2_start = models.TimeField(blank=True, null=True)
    time2_end = models.TimeField(blank=True, null=True)
    time3_start = models.TimeField(blank=True, null=True)
    time3_end = models.TimeField(blank=True, null=True)
    time4_start = models.TimeField(blank=True, null=True)
    time4_end = models.TimeField(blank=True, null=True)
    computer = models.ManyToManyField(Computer)


class DailyCheckIn(models.Model):
    postgraduate = models.ForeignKey(Postgraduate)
    date = models.DateField()
    check1 = models.TimeField(blank=True, null=True)
    check2 = models.TimeField(blank=True, null=True)
    check3 = models.TimeField(blank=True, null=True)
    check4 = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.postgraduate.name + self.date.strftime(" %Y-%m-%d")
