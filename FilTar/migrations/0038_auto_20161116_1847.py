# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 18:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FilTar', '0037_auto_20161116_1845'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contextpp',
            old_name='transcript_id',
            new_name='mrna',
        ),
    ]
