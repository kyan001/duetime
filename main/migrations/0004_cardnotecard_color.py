# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-14 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20171210_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardnotecard',
            name='color',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
