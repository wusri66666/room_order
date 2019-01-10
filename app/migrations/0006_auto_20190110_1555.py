# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-10 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20190110_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserverecord',
            name='timeline',
            field=models.IntegerField(choices=[(1, '8:00'), (2, '9:00'), (3, '10:00'), (4, '11:00'), (5, '12:00'), (6, '13:00'), (7, '14:00'), (8, '15:00'), (9, '16:00'), (10, '17:00')], verbose_name='预定时间'),
        ),
    ]