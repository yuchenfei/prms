# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-24 00:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailycheckinsetting',
            name='computer',
            field=models.ManyToManyField(blank=True, to='checkin.Computer'),
        ),
        migrations.AlterField(
            model_name='tempcheckinsetting',
            name='computer',
            field=models.ManyToManyField(blank=True, to='checkin.Computer'),
        ),
    ]
