from django.db import models


class Teacher(models.Model):
    username = models.CharField(max_length=30, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')  # 密码摘要
    salt = models.CharField(max_length=64)  # 盐
    group = models.ForeignKey('Group', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='课题组')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师'

    def __str__(self):
        return self.username

    @property
    def is_leader(self):
        return Group.objects.filter(leader=self).exists()


class Postgraduate(models.Model):
    pid = models.CharField(max_length=30, unique=True, verbose_name='学号')
    password = models.CharField(max_length=64, verbose_name='密码')  # 密码摘要
    salt = models.CharField(max_length=64)  # 盐
    name = models.CharField(max_length=50, verbose_name='姓名')
    teacher = models.ForeignKey('Teacher', verbose_name='导师')

    class Meta:
        verbose_name = '研究生'
        verbose_name_plural = '研究生'

    def __str__(self):
        return '(' + self.pid + ')' + self.name


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='组名')
    leader = models.OneToOneField('Teacher', related_name='lead_group', verbose_name='组长')

    # teacher_member = models.ManyToManyField('Teacher', blank=True, verbose_name='教师成员')

    class Meta:
        verbose_name = '课题组'
        verbose_name_plural = '课题组'

    def __str__(self):
        return self.name
