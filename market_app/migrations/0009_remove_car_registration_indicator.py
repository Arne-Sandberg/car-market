# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-10 08:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0008_auto_20180809_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='registration_indicator',
        ),
    ]