# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-04 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FilTar', '0047_auto_20161204_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='species',
            name='common_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='species',
            name='taxonomic_id',
            field=models.CharField(blank=True, db_column='taxonomic_ID', default='tax_ID', max_length=20, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
