# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-02 13:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='video',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='videos',
        ),
    ]
