# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-17 06:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MarketApp', '0037_auto_20180817_0639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='colour',
            field=models.CharField(choices=[('aqua', 'aqua'), ('black', 'black'), ('blue', 'blue'), ('fuchsia', 'fuchsia'), ('green', 'green'), ('gray', 'gray'), ('lime', 'lime'), ('maroon', 'maroon'), ('navy', 'navy'), ('olive', 'olive'), ('purple', 'purple'), ('red', 'red'), ('silver', 'silver'), ('teal', 'teal'), ('white', 'white'), ('yellow', 'yellow')], max_length=70),
        ),
    ]