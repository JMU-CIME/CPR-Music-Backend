from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import AssignmentSerializer
from teleband.assignments.api.serializers import ActivitySerializer

from teleband.assignments.models import Assignment, Activity
from teleband.courses.models import Course
from teleband.utils.permissions import IsTeacher


class ActivityViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
    lookup_field = "id"
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return self.queryset.filter(
            pk__in=Assignment.objects.filter(
                enrollment__course__slug=self.kwargs["course_slug_slug"]
            )
            .distinct("activity")
            .values_list("pk", flat=True)
        )


class AssignmentViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        course = Course.objects.get(slug=self.kwargs["course_slug_slug"])
        role = self.request.user.enrollment_set.get(course=course).role

        if role.name == "Student":
            return Assignment.objects.filter(
                enrollment__course=course, enrollment__user=self.request.user
            )
        if role.name == "Teacher":
            return Assignment.objects.filter(enrollment__course=course)
