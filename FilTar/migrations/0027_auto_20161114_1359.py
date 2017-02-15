# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 13:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FilTar', '0026_auto_20161114_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiments',
            name='tissue_name',
        ),
        migrations.AddField(
            model_name='experiments',
            name='tissue',
            field=models.ForeignKey(blank=True, max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='FilTar.Tissues'),
        ),
    ]