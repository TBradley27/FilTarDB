# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 11:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FilTar', '0003_auto_20161027_1702'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mirnas',
            options={'managed': False, 'verbose_name_plural': ' miRNAs'},
        ),
        migrations.AlterModelOptions(
            name='mrnas',
            options={'managed': False, 'verbose_name_plural': ' mRNAs'},
        ),
    ]