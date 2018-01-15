from django.db import models

from account.models import Postgraduate


def brief_directory_path(instance, filename):
    return 'uploads/brief/{0}/{1}'.format(instance.submitter.id, filename)


class Brief(models.Model):
    submitter = models.ForeignKey(Postgraduate)  # 提交小结的研究生
    date = models.DateField()  # 提交/最后修改时间
    content = models.TextField()  # 小结文本内容
    file = models.FileField(blank=True, null=True, upload_to=brief_directory_path)  # 小结附件
    commit = models.BooleanField(default=False)  # 提交状态
    have_read = models.BooleanField(default=False)  # 教师查阅状态
    instructions = models.TextField(blank=True, null=True)  # 教师批注
