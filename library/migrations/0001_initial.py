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
                ('a_id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('roma', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('d_id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('l_id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Maker',
            fields=[
                ('m_id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('s_id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('t_id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('t_type', models.PositiveIntegerField(choices=[(5, 'Others'), (0, 'Situation'), (1, 'Actress Type'), (2, 'Costume'), (3, 'Genre'), (4, 'Play')], default=5)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('cid', models.CharField(serialize=False, max_length=20, primary_key=True)),
                ('released_date', models.DateField()),
                ('runtime', models.DurationField()),
                ('title', models.TextField()),
                ('display_id', models.SlugField(max_length=20)),
                ('actresses', models.ManyToManyField(to='library.Actress', blank=True)),
                ('director', models.ForeignKey(blank=True, to='library.Director', null=True)),
                ('label', models.ForeignKey(blank=True, to='library.Label', null=True)),
                ('maker', models.ForeignKey(to='library.Maker')),
                ('series', models.ForeignKey(blank=True, to='library.Series', null=True)),
                ('tags', models.ManyToManyField(to='library.Tag', blank=True)),
            ],
        ),
    ]
