# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-21 03:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('svn_permission', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mod_name', models.CharField(choices=[(b'Core2', ((b'JCore', b'JCore'), (b'JCore/BL_Common', b'JCore/BL_Common'), (b'JCore/BL', b'JCore/BL'), (b'JCore/Common', b'JCore/Common'))), (b'Ops2', ((b'Ops', b'Ops'), (b'DevOps/Build', b'DevOps/Build'), (b'DevOps/Deploy', b'DevOps/Deploy'))), (b'Pws2', ((b'PWS', b'PWS'),)), (b'Test2', ((b'Scripts', b'Scripts'), (b'Tools', b'Tools')))], max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('repo_name', models.CharField(choices=[(0, b'all'), (1, b'core2'), (2, b'ops2'), (3, b'pws2'), (4, b'test2')], max_length=5, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'repositories',
            },
        ),
        migrations.AlterModelOptions(
            name='branch',
            options={'ordering': ['-branch_name'], 'verbose_name_plural': 'branches'},
        ),
        migrations.AddField(
            model_name='repository',
            name='branches',
            field=models.ManyToManyField(to='svn_permission.Branch'),
        ),
        migrations.AddField(
            model_name='module',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='svn_permission.Repository'),
        ),
    ]
