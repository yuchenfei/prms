from datetime import datetime
from django.db import models

from account.models import Postgraduate, Teacher


class Leave(models.Model):
    postgraduate = models.ForeignKey(Postgraduate)
    date = models.DateField()
    excuse = models.TextField()
    state = models.NullBooleanField(null=True)
    auditor = models.ForeignKey(Teacher, blank=True, null=True)  # 审核教师
    time_of_submission = models.DateTimeField()  # 申请提交时间
    time_of_processing = models.DateTimeField(blank=True, null=True)  # 批复时间

    def approve(self, teacher):
        self.state = True
        self.auditor = teacher
        self.time_of_processing = datetime.now()
        self.save()

    def reject(self, teacher):
        self.state = False
        self.auditor = teacher
        self.time_of_processing = datetime.now()
        self.save()
