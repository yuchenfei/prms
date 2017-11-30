from django.db import models


class Teacher(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=100)


class Postgraduate(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=100)
