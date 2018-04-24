from rest_framework import serializers

from apps.workout_tracker.models import (
    LOG_STATUS_CHOICES,
    Exercise,
    ExerciseType,
    Workout,
    WorkoutLog
)


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


class ExerciseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseType
        fields = ('name', 'weight_progression')


class ExerciseSerializer(serializers.ModelSerializer):
    exercise_type = ExerciseTypeSerializer(read_only=True)

    class Meta:
        model = Exercise
        fields = ('sets', 'reps', 'is_amrap', 'exercise_type')


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Workout

        fields = (
            'exercises',
        )


def _get_next_workout_id():
    return 1


class WorkoutLogsSerializer(serializers.ModelSerializer):
    status = ChoiceField(choices=LOG_STATUS_CHOICES, default=0)
    workout = WorkoutSerializer(read_only=True)

    class Meta:
        model = WorkoutLog
        depth = 10

        fields = (
            'id',
            'status',
            'workout_id',
            'workout',
            'finished_at',
            'created_at',
            'updated_at'
        )

    def create(self, validated_data):
        """ What we want here:
            - create workout log
            - create exercise logs for workout log with calculated weights
        """
        validated_data['workout_id'] =  _get_next_workout_id()

        workout_log = WorkoutLog.objects.create(**validated_data)
        # _create_exercise_logs_for_workout_log(workout_log.id)

        return workout_log

    def validate(self, data):
        if not self.instance:
            has_active_log = WorkoutLog.objects.filter(status__lt=2).count()
            if has_active_log:
                raise serializers.ValidationError(
                    'Only 1 active WorkoutLog allowed'
                )
        return data
