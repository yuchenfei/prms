# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-05 13:11
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
            name='CheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('forenoon_in', models.TimeField(blank=True, null=True)),
                ('forenoon_out', models.TimeField(blank=True, null=True)),
                ('afternoon_in', models.TimeField(blank=True, null=True)),
                ('afternoon_out', models.TimeField(blank=True, null=True)),
                ('postgraduate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Postgraduate')),
            ],
        ),
    ]
