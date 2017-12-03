from django.db import models


class Teacher(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Postgraduate(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey('Teacher')
    group = models.ForeignKey('Group', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField('Teacher')

    def __str__(self):
        return self.name
