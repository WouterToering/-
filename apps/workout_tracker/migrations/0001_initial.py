# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-22 13:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(db_index=True, editable=False)),
                ('updated_at', models.DateTimeField(db_index=True, editable=False)),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(db_index=True, editable=False)),
                ('updated_at', models.DateTimeField(db_index=True, editable=False)),
                ('name', models.CharField(max_length=200)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout_tracker.Program')),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(db_index=True, editable=False)),
                ('updated_at', models.DateTimeField(db_index=True, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout_tracker.Week')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='workout',
            unique_together=set([('week', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='week',
            unique_together=set([('program', 'name')]),
        ),
    ]