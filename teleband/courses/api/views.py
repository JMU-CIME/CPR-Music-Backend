import logging

from django.contrib.auth import get_user_model
from rest_framework import permissions
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
    RosterSerializer,
)
from teleband.assignments.api.serializers import AssignmentSerializer

from teleband.courses.models import Enrollment, Course
from teleband.assignments.models import Assignment, Activity
from teleband.musics.models import Piece, Part
from teleband.utils.permissions import IsTeacher

logger = logging.getLogger(__name__)

class IsTeacherEnrollment(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action not in ["update", "partial_update", "destroy"]:
            return True
        try:
            print("The get object {}".format(view.get_object()))
            e = Enrollment.objects.get(user=request.user, course=view.get_object().course)
            return e.role.name == "Teacher"
        except Enrollment.DoesNotExist:
            logger.info(
                "No Enrollment for {} in {}".format(
                    request.user, view.get_object()
                )
            )
        return False



class EnrollmentViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.all()
    permission_classes = [IsTeacherEnrollment]


    def get_queryset(self, *args, **kwargs):
        if self.action in ["update", "partial_update", "destroy"]:
            courses = [e.course for e in Enrollment.objects.filter(user=self.request.user, role__name="Teacher")]
            return self.queryset.filter(course__in=courses)

        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "update" or self.action == "partial_update":
            return EnrollmentInstrumentSerializer
        return self.serializer_class


class CoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "retrieve":
            return True
        try:
            e = Enrollment.objects.get(user=request.user, course=view.get_object())
            return e.role.name == "Teacher"
        except Enrollment.DoesNotExist:
            logger.info(
                "No Enrollment for {} in {}".format(
                    request.user, view.get_object()
                )
            )
        return False


class CourseViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    lookup_field = "slug"
    permission_classes = [CoursePermission]

    def get_serializer_class(self):
        if self.action == "create":
            return CourseRelatedSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True)
    def roster(self, request, **kwargs):
        course_enrollments = Enrollment.objects.filter(course=self.get_object())
        serializer = RosterSerializer(
            course_enrollments, many=True, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True, methods=["post"])
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
