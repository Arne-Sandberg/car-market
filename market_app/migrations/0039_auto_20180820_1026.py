# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-20 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0038_auto_20180817_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='number_of_seats',
            field=models.IntegerField(default=4),
        ),
    ]
