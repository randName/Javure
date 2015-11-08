# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actress',
            options={'verbose_name_plural': 'actresses'},
        ),
        migrations.AlterModelOptions(
            name='series',
            options={'verbose_name_plural': 'series'},
        ),
        migrations.AlterField(
            model_name='actress',
            name='_id',
            field=models.PositiveIntegerField(serialize=False, primary_key=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='actress',
            name='furi',
            field=models.CharField(blank=True, max_length=50, verbose_name='振り仮名'),
        ),
        migrations.AlterField(
            model_name='actress',
            name='roma',
            field=models.CharField(blank=True, max_length=50, verbose_name='ローマ字'),
        ),
        migrations.AlterField(
            model_name='director',
            name='_id',
            field=models.PositiveIntegerField(serialize=False, primary_key=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='label',
            name='_id',
            field=models.PositiveIntegerField(serialize=False, primary_key=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='maker',
            name='_id',
            field=models.PositiveIntegerField(serialize=False, primary_key=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='maker',
            name='url',
            field=models.URLField(blank=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='series',
            name='_id',
            field=models.PositiveIntegerField(serialize=False, primary_key=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='_id',
            field=models.PositiveIntegerField(serialize=False, primary_key=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='video',
            name='cid',
            field=models.CharField(serialize=False, primary_key=True, max_length=20, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='video',
            name='display_id',
            field=models.SlugField(max_length=20, verbose_name='Display ID'),
        ),
        migrations.AlterField(
            model_name='video',
            name='released_date',
            field=models.DateField(verbose_name='Released Date'),
        ),
    ]
