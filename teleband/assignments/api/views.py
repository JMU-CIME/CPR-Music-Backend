from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import AssignmentSerializer

from teleband.assignments.models import Assignment


class AssignmentViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    lookup_field = "id"
