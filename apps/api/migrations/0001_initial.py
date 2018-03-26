# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-26 14:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imei', models.CharField(blank=True, max_length=15, null=True)),
                ('postgraduate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.Postgraduate')),
            ],
        ),
    ]
