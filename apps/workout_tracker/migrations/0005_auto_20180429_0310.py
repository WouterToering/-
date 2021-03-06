# Generated by Django 2.0.4 on 2018-04-29 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workout_tracker', '0004_auto_20180429_0221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exerciselog',
            name='workout',
        ),
        migrations.AddField(
            model_name='exerciselog',
            name='workout_log',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='exercise_logs', to='workout_tracker.WorkoutLog'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exerciselog',
            name='weight',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
    ]
