# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-02 02:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('svn_permission', '0005_auto_20180401_2159'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupperm',
            options={'verbose_name': 'Group Permission', 'verbose_name_plural': 'Group Permissions'},
        ),
    ]