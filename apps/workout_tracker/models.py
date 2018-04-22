from django.db import models

from apps.main.model_mixins import ModelMixinBundle


class Program(ModelMixinBundle):
    name = models.CharField(
        db_index=True,
        unique=True,
        null=False,
        blank=False,
        max_length=200
    )


class Week(ModelMixinBundle):
    program = models.ForeignKey('Program', on_delete=models.CASCADE)

    name = models.CharField(
        db_index=True,
        null=False,
        blank=False,
        max_length=200
    )
    position = models.PositiveSmallIntegerField(null=False)

    class Meta:
        unique_together = ('program', 'name')


class Workout(ModelMixinBundle):
    week = models.ForeignKey('Week', on_delete=models.CASCADE)

    name = models.CharField(
        db_index=True,
        null=False,
        blank=False,
        max_length=100
    )
    position = models.PositiveSmallIntegerField(null=False)

    class Meta:
        unique_together = ('week', 'name')


class Exercise(ModelMixinBundle):
    name = models.CharField(
        db_index=True,
        null=False,
        blank=False,
        max_length=100
    )
    weight_progression = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=False
    )


class ExerciseVolume(ModelMixinBundle):
    sets = models.PositiveSmallIntegerField()
    reps = models.PositiveSmallIntegerField()
    weight_multiplier = models.DecimalField(max_digits=3, decimal_places=2)
    is_amrap = models.BooleanField()

    exercise = models.ForeignKey('Exercise')
    workout = models.ForeignKey('Workout', related_name='exercises')
    position = models.PositiveSmallIntegerField(null=False)
