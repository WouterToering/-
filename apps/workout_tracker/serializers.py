from rest_framework import serializers

from apps.workout_tracker.models import Program


class ProgramSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Program

        fields = (
            'id',
            'name',
        )
        lookup_field='id'
