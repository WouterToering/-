from decimal import Decimal

from django.db import DatabaseError, transaction
from rest_framework import serializers

from apps.workout_tracker.models import (
    Exercise,
    ExerciseLog,
    ExerciseType,
    LOG_STATUS_CHOICES,
    LogStatus,
    Week,
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
    latest_workout_log = WorkoutLog.objects.last()
    if latest_workout_log is None:
        return Week.objects.first().workouts.first().id

    workouts_in_week = list(latest_workout_log.workout.week.workouts.all())
    workout_index = workouts_in_week.index(latest_workout_log.workout)

    if workout_index < len(workouts_in_week)-1:
        return workouts_in_week[workout_index+1].id

    # Go to the next week
    weeks = list(Week.objects.all())
    week_index = weeks.index(latest_workout_log.workout.week)

    if week_index < len(weeks)-1:
        return weeks[week_index+1].workouts.first().id

    # First week, first workout
    return weeks[0].workouts.first().id


def _create_exercise_logs_for_workout_log(workout_log_id, workout_id):
    workout = Workout.objects.get(id=workout_id)

    try:
        previous_workout_log = WorkoutLog.objects.order_by('-id')[1]
    except IndexError:
        previous_workout_log = None
    should_increase_weight = (
        previous_workout_log is not None and
        previous_workout_log.workout.week_id != workout.week_id
    )

    for exercise in workout.exercises.all():
        weight = 20.0  # random starting number
        latest_exercise_log = ExerciseLog.objects.filter(
            exercise__exercise_type_id=exercise.exercise_type_id
        ).last()

        if latest_exercise_log is not None:
            weight = (
                latest_exercise_log.weight *
                exercise.weight_multiplier /
                latest_exercise_log.exercise.weight_multiplier
            )
            weight = weight - weight % Decimal(2.5)  # 1.25kg = lightest plate

            if (should_increase_weight and
                    latest_exercise_log.status == LogStatus.FINISHED.value):
                weight = weight + exercise.exercise_type.weight_progression

        ExerciseLog.objects.create(
            exercise_id=exercise.id,
            workout_log_id=workout_log_id,
            status=LogStatus.FINISHED.value,
            weight=weight
        )


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
        for i in range(7):
            validated_data['workout_id'] = _get_next_workout_id()

            try:
                with transaction.atomic():
                    validated_data['status'] = LogStatus.FINISHED.value
                    workout_log = WorkoutLog.objects.create(**validated_data)
                    _create_exercise_logs_for_workout_log(
                        workout_log.id, validated_data['workout_id']
                    )
            except DatabaseError:
                return WorkoutLog(**validated_data)  # nice django error pls

        return workout_log

    def validate(self, data):
        if not self.instance:
            has_active_log = WorkoutLog.objects.filter(status__lt=2).count()
            if has_active_log:
                raise serializers.ValidationError(
                    'Only 1 active WorkoutLog allowed'
                )
        return data
