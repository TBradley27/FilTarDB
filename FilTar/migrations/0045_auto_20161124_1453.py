# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FilTar', '0044_remove_contextpp_tpm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contextpp',
            name='species',
            field=models.CharField(blank=True, db_column='Species', max_length=20, null=True),
        ),
    ]
