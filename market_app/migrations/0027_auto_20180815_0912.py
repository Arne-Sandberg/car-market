# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-15 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0026_auto_20180815_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(default=1),
        ),
    ]