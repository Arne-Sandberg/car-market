# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-10 12:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0011_auto_20180810_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
