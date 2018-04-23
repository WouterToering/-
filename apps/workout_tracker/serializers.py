from rest_framework import serializers

from apps.workout_tracker.models import LOG_STATUS_CHOICES, WorkoutLog


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, data):
        if data not in self.choices.keys():
            self.fail('invalid_choice', input=data)
        else:
            return self.choices[data]

    def to_internal_value(self, data):
        for key, value in self.choices.items():
            if value == data:
                return key
        self.fail('invalid_choice', input=data)


class WorkoutLogsSerializer(serializers.ModelSerializer):
    status = ChoiceField(choices=LOG_STATUS_CHOICES, default=0)

    class Meta:
        model = WorkoutLog
        depth = 0

        fields = (
            'id',
            'status',
            'workout_id',
            'workout',
            'finished_at',
            'created_at',
            'updated_at'
        )

    def validate(self, data):
        if not self.instance:
            has_active_log = WorkoutLog.objects.filter(status__lt=2).count()
            if has_active_log:
                raise serializers.ValidationError(
                    'Only 1 active WorkoutLog allowed'
                )
        return data
