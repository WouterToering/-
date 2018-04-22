from django.db.models import QuerySet
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.main.metadata import MinimalMetadata
from apps.workout_tracker.models import Program
from apps.workout_tracker.serializers import ProgramSerializer


class ProgramAPIViewSet(ModelViewSet):
    model = Program
    renderer_classes = (JSONRenderer,)
    serializer_class = ProgramSerializer
    metadata_class = MinimalMetadata

    def get_queryset(self) -> QuerySet:
        return Program.objects.all()

    def list(self, request, *args, **kwargs) -> Response:
        programs = self.get_queryset()
        serializer = self.get_serializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
