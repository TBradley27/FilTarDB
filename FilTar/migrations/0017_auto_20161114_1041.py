# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FilTar', '0016_auto_20161114_1040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mrnas',
            name='id',
        ),
        migrations.AlterField(
            model_name='mrnas',
            name='mrna_id',
            field=models.CharField(blank=True, db_column='mRNA_ID', default='mrnas', max_length=20, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]