from django.db import models

from account.models import Group, Teacher


def group_directory_path(instance, filename):
    return 'uploads/group/{0}/{1}'.format(instance.group.id, filename)


class GroupFile(models.Model):
    title = models.CharField(max_length=20, unique=True)
    group = models.ForeignKey(Group)
    owner = models.ForeignKey(Teacher)
    describe = models.CharField(max_length=50)
    file = models.FileField(upload_to=group_directory_path)
    date = models.DateTimeField()
    show = models.BooleanField(default=False)
