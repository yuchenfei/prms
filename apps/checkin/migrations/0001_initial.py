# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-24 15:20
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
            name='Computer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('cpu_id', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DailyCheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('check1', models.TimeField(blank=True, null=True)),
                ('check2', models.TimeField(blank=True, null=True)),
                ('check3', models.TimeField(blank=True, null=True)),
                ('check4', models.TimeField(blank=True, null=True)),
                ('postgraduate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Postgraduate')),
            ],
        ),
        migrations.CreateModel(
            name='DailyCheckInSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('week_option', models.CharField(max_length=7)),
                ('times', models.IntegerField(choices=[(1, '单次签到'), (2, '一个时间段'), (4, '两个时间段')], default=1)),
                ('time1_start', models.TimeField()),
                ('time1_end', models.TimeField()),
                ('time2_start', models.TimeField(blank=True, null=True)),
                ('time2_end', models.TimeField(blank=True, null=True)),
                ('time3_start', models.TimeField(blank=True, null=True)),
                ('time3_end', models.TimeField(blank=True, null=True)),
                ('time4_start', models.TimeField(blank=True, null=True)),
                ('time4_end', models.TimeField(blank=True, null=True)),
                ('computer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checkin.Computer')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Teacher', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TempCheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('postgraduate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Postgraduate')),
            ],
        ),
        migrations.CreateModel(
            name='TempCheckInSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('computer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checkin.Computer')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Teacher')),
            ],
        ),
        migrations.AddField(
            model_name='tempcheckin',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkin.TempCheckInSetting'),
        ),
    ]
