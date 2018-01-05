from django.db import models


class Teacher(models.Model):
    username = models.CharField(max_length=30, primary_key=True, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')  # 密码摘要
    salt = models.CharField(max_length=64)  # 盐

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师'

    def __str__(self):
        return self.username

    @property
    def is_leader(self):
        return self.group_leader.filter(leader=self).exists()


class Postgraduate(models.Model):
    id = models.CharField(max_length=30, primary_key=True, verbose_name='学号')
    password = models.CharField(max_length=64, verbose_name='密码')  # 密码摘要
    salt = models.CharField(max_length=64)  # 盐
    name = models.CharField(max_length=50, verbose_name='姓名')
    teacher = models.ForeignKey('Teacher', verbose_name='导师')
    group = models.ForeignKey('Group', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='小组')

    class Meta:
        verbose_name = '研究生'
        verbose_name_plural = '研究生'

    def __str__(self):
        return '(' + self.id + ')' + self.name


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='组名')
    leader = models.ForeignKey('Teacher', related_name='group_leader', verbose_name='组长')
    members = models.ManyToManyField('Teacher', blank=True, related_name='group_members', verbose_name='教师组成')

    class Meta:
        verbose_name = '小组'
        verbose_name_plural = '小组'

    def __str__(self):
        return self.name
