# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-06 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0005_auto_20180806_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='car',
            name='registration_indicator',
            field=models.CharField(choices=[('New', 'N'), ('Used vehicle', 'U'), ('Re-registrated', 'R'), ('Scratch-built', 'S')], default='N', max_length=20),
        ),
    ]
