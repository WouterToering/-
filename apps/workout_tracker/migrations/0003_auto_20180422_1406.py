# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-22 14:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workout_tracker', '0002_auto_20180422_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, editable=False)),
                ('updated_at', models.DateTimeField(db_index=True, editable=False)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('weight_progression', models.DecimalField(decimal_places=1, max_digits=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExerciseVolume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, editable=False)),
                ('updated_at', models.DateTimeField(db_index=True, editable=False)),
                ('sets', models.PositiveSmallIntegerField()),
                ('reps', models.PositiveSmallIntegerField()),
                ('weight_multiplier', models.DecimalField(decimal_places=2, max_digits=3)),
                ('is_amrap', models.BooleanField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout_tracker.Exercise')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='program',
            name='name',
            field=models.CharField(db_index=True, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='week',
            name='name',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='workout',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AddField(
            model_name='exercisevolume',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout_tracker.Workout'),
        ),
    ]