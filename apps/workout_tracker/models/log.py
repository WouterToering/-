import enum

from django.db import models
from django.utils import timezone

from apps.main.model_mixins import ModelMixinBundle


class LogStatus(enum.Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    FINISHED = 2


LOG_STATUS_CHOICES = ((e.value, e.name) for e in list(LogStatus))


class WorkoutLog(ModelMixinBundle):
    status = models.PositiveSmallIntegerField(
        choices=LOG_STATUS_CHOICES,
        default=LogStatus.NOT_STARTED.value
    )
    finished_at = models.DateTimeField(db_index=True, editable=False)

    workout = models.ForeignKey('Workout')

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
    completed = models.NullBooleanField()

    workout = models.ForeignKey('WorkoutLog')
    exercise = models.ForeignKey('Exercise')

    def save(self, *args, **kwargs):
        if (kwargs.get('status') == LogStatus.FINISHED and self.status !=
                LogStatus.FINISHED):
            self.finished_at = timezone.now()

        return super().save(*args, **kwargs)
