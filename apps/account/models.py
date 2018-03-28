import uuid
from django.db import models


class Teacher(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    password = models.CharField(max_length=64, verbose_name='密码')  # 密码摘要
    salt = models.CharField(max_length=64)  # 盐
    name = models.CharField(max_length=30, verbose_name='姓名')
    school = models.CharField(max_length=30, blank=True, null=True, verbose_name='学校')
    specialty = models.CharField(max_length=30, blank=True, null=True, verbose_name='专业')
    group = models.ForeignKey('Group', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='课题组')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师'

    def __str__(self):
        return self.name

    @property
    def is_leader(self):
        return Group.objects.filter(leader=self).exists()


class Postgraduate(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    password = models.CharField(max_length=64, verbose_name='密码')  # 密码摘要
    salt = models.CharField(max_length=64)  # 盐
    name = models.CharField(max_length=50, verbose_name='姓名')
    teacher = models.ForeignKey('Teacher', verbose_name='导师')
    school = models.CharField(max_length=30, blank=True, null=True, verbose_name='学校')
    classes = models.CharField(max_length=30, blank=True, null=True, verbose_name='班级')

    class Meta:
        verbose_name = '研究生'
        verbose_name_plural = '研究生'

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='组名')
    leader = models.OneToOneField('Teacher', related_name='lead_group', verbose_name='组长')

    class Meta:
        verbose_name = '课题组'
        verbose_name_plural = '课题组'

    def __str__(self):
        return self.name
