# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 14:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FilTar', '0028_auto_20161114_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genomeassembly',
            name='common_name',
        ),
        migrations.AddField(
            model_name='genomeassembly',
            name='species',
            field=models.ForeignKey(blank=True, max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='FilTar.Species'),
        ),
    ]
