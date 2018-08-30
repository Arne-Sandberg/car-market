# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-09 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0007_auto_20180807_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='registration_indicator',
            field=models.CharField(choices=[('New', 'N'), ('Used vehicle', 'U'), ('Re-registered', 'R'), ('Scratch-built', 'S')], default='N', max_length=20),
        ),
    ]