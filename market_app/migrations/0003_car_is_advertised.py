# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-06 10:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0002_auto_20180803_0818'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='is_advertised',
            field=models.BooleanField(default=False),
        ),
    ]