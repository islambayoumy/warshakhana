# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-26 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20170325_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rates',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterUniqueTogether(
            name='rates',
            unique_together=set([('ip', 'workshop')]),
        ),
    ]
