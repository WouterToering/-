# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-23 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutlog',
            name='finished_at',
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]