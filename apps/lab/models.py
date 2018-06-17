from django.db import models


class Experiment(models.Model):
    name = models.CharField(max_length=64, verbose_name='名称')
    content = models.CharField(max_length=255, verbose_name='内容')
    num = models.IntegerField(verbose_name='最大人数')
    classes = models.CharField(max_length=30, verbose_name='班级')

    class Meta:
        verbose_name = '实验'
        verbose_name_plural = '实验'


class Grade(models.Model):
    classes = models.CharField(max_length=30, verbose_name='班级')
    name = models.CharField(max_length=30, verbose_name='姓名')
    ex_name = models.CharField(max_length=64, verbose_name='实验名称')
    grade = models.CharField(max_length=30, verbose_name='成绩')
    commment = models.CharField(max_length=64, verbose_name='评语')

    class Meta:
        verbose_name = '成绩'
        verbose_name_plural = '成绩'
