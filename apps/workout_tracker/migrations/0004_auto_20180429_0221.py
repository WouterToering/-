# Generated by Django 2.0.4 on 2018-04-29 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workout_tracker', '0003_auto_20180424_2134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exercise',
            options={'ordering': ('position',)},
        ),
        migrations.AlterModelOptions(
            name='workout',
            options={'ordering': ('position',)},
        ),
        migrations.AlterField(
            model_name='exerciselog',
            name='amrap_reps',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='week',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workouts', to='workout_tracker.Week'),
        ),
    ]
