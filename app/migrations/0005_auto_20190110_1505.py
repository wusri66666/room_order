# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-10 07:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20190110_1501'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reserverecord',
            old_name='meeting_room',
            new_name='room',
        ),
        migrations.RenameField(
            model_name='reserverecord',
            old_name='time',
            new_name='timeline',
        ),
        migrations.AlterUniqueTogether(
            name='reserverecord',
            unique_together=set([('data', 'timeline', 'room')]),
        ),
    ]
