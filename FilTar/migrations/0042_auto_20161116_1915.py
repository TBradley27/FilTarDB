# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 19:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FilTar', '0041_auto_20161116_1914'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contextpp',
            old_name='common_name',
            new_name='species',
        ),
    ]