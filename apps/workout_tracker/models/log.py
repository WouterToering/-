import enum

from django.db import models
from django.utils import timezone

from apps.main.model_mixins import ModelMixinBundle


class LogStatus(enum.Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    FINISHED = 2
    FAILED = 3


LOG_STATUS_CHOICES = tuple((e.value, e.name) for e in list(LogStatus))


class WorkoutLog(ModelMixinBundle):
    status = models.PositiveSmallIntegerField(
        choices=LOG_STATUS_CHOICES,
        default=LogStatus.NOT_STARTED.value
    )
    finished_at = models.DateTimeField(editable=False, null=True)

    workout = models.ForeignKey('Workout', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if (kwargs.get('status') == LogStatus.FINISHED and self.status !=
                LogStatus.FINISHED):
            self.finished_at = timezone.now()

        return super().save(*args, **kwargs)


class ExerciseLog(ModelMixinBundle):
    status = models.PositiveSmallIntegerField(
        choices=LOG_STATUS_CHOICES,
        default=LogStatus.NOT_STARTED.value
    )
    weight = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=False
    )
    amrap_reps = models.PositiveSmallIntegerField(null=True)

    workout_log = models.ForeignKey(
        'WorkoutLog',
        on_delete=models.CASCADE,
        related_name='exercise_logs'
    )
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if (kwargs.get('status') == LogStatus.FINISHED and self.status !=
                LogStatus.FINISHED):
            self.finished_at = timezone.now()

        return super().save(*args, **kwargs)
