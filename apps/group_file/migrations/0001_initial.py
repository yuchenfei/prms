# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-12 16:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import group_file.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, unique=True)),
                ('describe', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to=group_file.models.group_directory_path)),
                ('date', models.DateTimeField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Group')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Teacher')),
            ],
        ),
    ]
