from django.db import models

from apps.main.model_mixins import ModelMixinBundle


class Program(ModelMixinBundle):
    objects = models.Manager()

    name = models.CharField(
        db_index=True,
        unique=True,
        null=False,
        blank=False,
        max_length=200
    )


class Week(ModelMixinBundle):
    objects = models.Manager()

    program = models.ForeignKey('Program', on_delete=models.CASCADE)

    name = models.CharField(
        db_index=True,
        null=False,
        blank=False,
        max_length=200
    )

    class Meta:
        unique_together = ('program', 'name')


class Workout(ModelMixinBundle):
    objects = models.Manager()

    week = models.ForeignKey('Week', on_delete=models.CASCADE)

    name = models.CharField(
        db_index=True,
        null=False,
        blank=False,
        max_length=100
    )

    class Meta:
        unique_together = ('week', 'name')


class Exercise(ModelMixinBundle):
    objects = models.Manager()

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
    objects = models.Manager()

    sets = models.PositiveSmallIntegerField()
    reps = models.PositiveSmallIntegerField()
    weight_multiplier = models.DecimalField(max_digits=3, decimal_places=2)
    is_amrap = models.BooleanField()

    exercise = models.ForeignKey('Exercise')
    workout = models.ForeignKey('Workout', related_name='exercises')
