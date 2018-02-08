# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-06 01:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('checkin', '0002_computer'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckInSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_type', models.IntegerField(choices=[(1, 'Daily Check In'), (2, 'Meeting Check In')])),
                ('enable', models.BooleanField(default=False)),
                ('date_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='MeetingCheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('postgraduate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Postgraduate')),
            ],
        ),
        migrations.RenameModel(
            old_name='CheckIn',
            new_name='DailyCheckIn',
        ),
        migrations.AlterField(
            model_name='computer',
            name='cpu_id',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AddField(
            model_name='checkinsetting',
            name='computer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checkin.Computer'),
        ),
        migrations.AddField(
            model_name='checkinsetting',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Teacher'),
        ),
    ]
