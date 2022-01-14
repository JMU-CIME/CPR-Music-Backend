import logging

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import (
    EnrollmentSerializer,
    CourseSerializer,
    CourseRelatedSerializer,
    EnrollmentInstrumentSerializer,
)
from teleband.assignments.api.serializers import AssignmentSerializer

from teleband.courses.models import Enrollment, Course
from teleband.assignments.models import Assignment, Activity
from teleband.musics.models import Piece, Part
from teleband.utils.permissions import IsTeacher

logger = logging.getLogger(__name__)


class EnrollmentViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.all()

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "update" or self.action == "partial_update":
            return EnrollmentInstrumentSerializer
        return self.serializer_class


class CourseViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    lookup_field = "slug"
    permission_classes = [IsTeacher]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CourseRelatedSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True)
    def roster(self, request, **kwargs):
        course_enrollments = Enrollment.objects.filter(course=self.get_object())
        serializer = EnrollmentSerializer(
            course_enrollments, many=True, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True)
    def assign(self, request, **kwargs):
        if "piece_id" not in request.POST:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Missing piece_id in POST data"},
            )

        try:
            piece = Piece.objects.get(pk=request.POST["piece_id"])
        except Piece.DoesNotExist:
            logger.info(
                "Attempt to assign non-existent piece {}".format(
                    request.POST["piece_id"]
                )
            )
            return Response(status=status.HTTP_404_NOT_FOUND)

        course = self.get_object()

        assignments = []
        for activity in Activity.objects.all():
            # Get this piece’s part for this kind of activity
            part = Part.objects.get(piece=piece, part_type=activity.part_type)
            for e in Enrollment.objects.filter(course=course, role__name="Student"):
                assignments.append(
                    Assignment.objects.create(
                        activity=activity,
                        enrollment=e,
                        instrument=e.instrument,
                        part=part,
                    )
                )

        serializer = AssignmentSerializer(
            assignments, many=True, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)
