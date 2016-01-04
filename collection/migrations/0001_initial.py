# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 08:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('library', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filesize', models.PositiveIntegerField(blank=True, null=True, verbose_name='size (MB)')),
                ('height', models.PositiveIntegerField(blank=True, null=True)),
                ('width', models.PositiveIntegerField(blank=True, null=True)),
                ('container', models.PositiveIntegerField(choices=[(0, 'Others'), (1, '.mp4'), (2, '.mkv'), (3, '.avi'), (4, '.wmv'), (6, '.rmvb'), (5, 'Disc Image')], default=0)),
                ('has_watermarks', models.BooleanField()),
                ('has_subtitles', models.BooleanField()),
                ('has_adverts', models.BooleanField()),
                ('parts', models.PositiveIntegerField(default=1)),
                ('remarks', models.TextField(blank=True)),
                ('video', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='library.Video')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actresses', models.ManyToManyField(blank=True, to='library.Actress')),
                ('directors', models.ManyToManyField(blank=True, to='library.Director')),
                ('items', models.ManyToManyField(blank=True, to='collection.Item')),
                ('keywords', models.ManyToManyField(blank=True, to='library.Keyword')),
                ('labels', models.ManyToManyField(blank=True, to='library.Label')),
                ('makers', models.ManyToManyField(blank=True, to='library.Maker')),
                ('series', models.ManyToManyField(blank=True, to='library.Series')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('videos', models.ManyToManyField(blank=True, to='library.Video')),
            ],
        ),
    ]
