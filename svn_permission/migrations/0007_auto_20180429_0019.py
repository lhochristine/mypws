# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-29 04:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svn_permission', '0006_auto_20180401_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='branch_name',
            field=models.CharField(default='trunk', max_length=32, primary_key=True, serialize=False),
        ),
    ]
