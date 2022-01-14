from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import EnrollmentSerializer, CourseSerializer, CourseRelatedSerializer
from teleband.assignments.api.serializers import AssignmentSerializer

from teleband.courses.models import Enrollment, Course
from teleband.assignments.models import Assignment
from teleband.musics.models import Piece


class EnrollmentViewSet(
    ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.all()

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(user=self.request.user)


class CourseViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CourseRelatedSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # permission_class = IsTeacher
    @action(detail=True)
    def assign(self, request, **kwargs):
        if "piece_id" not in request.GET:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Missing piece_id in GET data"},
            )

        # piece = Piece.objects.get(pk=request.GET["piece_id"])
        # print("Assign activities for this piece {}".format(piece))

        # piece.activity_set

        return Response(status=status.HTTP_200_OK)
