# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-15 11:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MarketApp', '0027_auto_20180815_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]