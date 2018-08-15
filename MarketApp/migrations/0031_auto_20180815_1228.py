# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-15 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MarketApp', '0030_auto_20180815_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='stripe_public_key',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='stripe_secret_key',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
