# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-04 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FilTar', '0046_auto_20161204_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genomeassembly',
            name='species',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
