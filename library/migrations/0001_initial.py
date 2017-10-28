# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-28 10:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actress',
            fields=[
                ('_id', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('roma', models.CharField(blank=True, max_length=255, verbose_name='romaji')),
                ('furi', models.CharField(blank=True, max_length=255, verbose_name='furigana')),
                ('alias', models.CharField(blank=True, max_length=255, verbose_name='aliases')),
            ],
            options={
                'verbose_name_plural': 'actresses',
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('_id', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('_id', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.PositiveSmallIntegerField(choices=[(0, 'Situation'), (1, 'Actress Type'), (2, 'Costume'), (3, 'Genre'), (4, 'Play'), (5, 'Others')], default=5)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('_id', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Maker',
            fields=[
                ('_id', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('roma', models.CharField(blank=True, max_length=255, verbose_name='romaji')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('_id', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'series',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vid', models.SlugField(blank=True, max_length=255)),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('runtime', models.DurationField(blank=True, null=True)),
                ('released_date', models.DateField(blank=True, null=True)),
                ('actresses', models.ManyToManyField(blank=True, to='library.Actress')),
                ('director', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.Director')),
                ('keywords', models.ManyToManyField(blank=True, to='library.Keyword')),
                ('label', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.Label')),
                ('maker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Maker')),
                ('series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.Series')),
            ],
            options={
                'ordering': ['-released_date'],
            },
        ),
    ]
