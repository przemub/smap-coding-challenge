# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-21 13:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consumption', '0002_auto_20180821_0938'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consumptionentry',
            options={'ordering': ['user', 'datetime']},
        ),
    ]
