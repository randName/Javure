# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actress',
            fields=[
                ('_id', models.PositiveIntegerField(verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('roma', models.CharField(max_length=50, blank=True, verbose_name='ローマ字')),
                ('furi', models.CharField(max_length=20, blank=True, verbose_name='振り仮名')),
            ],
            options={
                'verbose_name_plural': 'actresses',
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('_id', models.PositiveIntegerField(verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('_id', models.PositiveIntegerField(verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('category', models.PositiveIntegerField(default=5, choices=[(0, 'Situation'), (1, 'Actress Type'), (2, 'Costume'), (3, 'Genre'), (4, 'Play'), (5, 'Others')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('_id', models.PositiveIntegerField(verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Maker',
            fields=[
                ('_id', models.PositiveIntegerField(verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('url', models.URLField(blank=True, verbose_name='URL')),
                ('description', models.TextField(blank=True)),
                ('roma', models.CharField(max_length=50, blank=True, verbose_name='ローマ字')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('_id', models.PositiveIntegerField(verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'series',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('pid', models.SlugField(verbose_name='Product ID', primary_key=True, serialize=False)),
                ('cid', models.SlugField(verbose_name='Content ID')),
                ('display_id', models.SlugField(max_length=20, verbose_name='Display ID')),
                ('released_date', models.DateField(verbose_name='Released Date')),
                ('runtime', models.DurationField()),
                ('title', models.TextField()),
                ('actresses', models.ManyToManyField(blank=True, to='library.Actress')),
                ('director', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='library.Director')),
                ('keywords', models.ManyToManyField(blank=True, to='library.Keyword')),
                ('label', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='library.Label')),
                ('maker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='library.Maker')),
                ('series', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='library.Series')),
            ],
            options={
                'ordering': ['-released_date'],
            },
        ),
    ]
