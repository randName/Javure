# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actress',
            fields=[
                ('_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('roma', models.CharField(blank=True, max_length=50)),
                ('furi', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Actresses',
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['_id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['_id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Maker',
            fields=[
                ('_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('url', models.URLField(blank=True)),
            ],
            options={
                'ordering': ['_id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Series',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('category', models.PositiveIntegerField(default=5, choices=[(5, 'Others'), (0, 'Situation'), (1, 'Actress Type'), (2, 'Costume'), (3, 'Genre'), (4, 'Play')])),
            ],
            options={
                'ordering': ['_id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('cid', models.CharField(primary_key=True, max_length=20, serialize=False)),
                ('released_date', models.DateField()),
                ('runtime', models.DurationField()),
                ('title', models.TextField()),
                ('display_id', models.SlugField(max_length=20)),
                ('actresses', models.ManyToManyField(blank=True, to='library.Actress')),
                ('director', models.ForeignKey(blank=True, null=True, to='library.Director')),
                ('label', models.ForeignKey(blank=True, null=True, to='library.Label')),
                ('maker', models.ForeignKey(to='library.Maker')),
                ('series', models.ForeignKey(blank=True, null=True, to='library.Series')),
                ('tags', models.ManyToManyField(blank=True, to='library.Tag')),
            ],
            options={
                'ordering': ['-released_date'],
            },
        ),
    ]
