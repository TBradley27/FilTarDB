# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 17:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FilTar', '0032_auto_20161114_1417'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expressionprofiles',
            old_name='transcript_id',
            new_name='mrnas',
        ),
    ]