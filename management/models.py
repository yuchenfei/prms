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
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField('Teacher')

    def __str__(self):
        return self.name


class CheckIn(models.Model):
    postgraduate = models.ForeignKey('Postgraduate')
    date = models.DateField()
    forenoon_in = models.TimeField(blank=True, null=True)
    forenoon_out = models.TimeField(blank=True, null=True)
    afternoon_in = models.TimeField(blank=True, null=True)
    afternoon_out = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.postgraduate.name + self.date.strftime(" %Y-%m-%d")


class Leave(models.Model):
    postgraduate = models.ForeignKey('Postgraduate')
    date = models.DateField()
    excuse = models.TextField()
    state = models.NullBooleanField(null=True)
    time_of_submission = models.DateTimeField()
    time_of_processing = models.DateTimeField(blank=True, null=True)


# class Brief(models.Model):
#     pass
