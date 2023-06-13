from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import AssignmentViewSetSerializer, AssignmentInstrumentSerializer, AssignmentSerializer
from teleband.assignments.api.serializers import ActivitySerializer
from teleband.musics.api.serializers import PartTranspositionSerializer

from teleband.assignments.models import Assignment, Activity
from teleband.courses.models import Course
from teleband.utils.permissions import IsTeacher


class TeacherUpdate(IsTeacher):
    def has_permission(self, request, view):
        if view.action not in ["update", "partial_update"]:
            return True

        return super().has_permission(request, view)


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


class AssignmentViewSet(
    RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet
):
    serializer_class = AssignmentViewSetSerializer
    queryset = Assignment.objects.all()
    lookup_field = "id"
    permission_classes = [TeacherUpdate]

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return AssignmentInstrumentSerializer
        elif self.action == "retrieve":
            return AssignmentSerializer
        return self.serializer_class

    @action(detail=True)
    def notation(self, request, *args, **kwargs):
        course = Course.objects.get(slug=self.kwargs["course_slug_slug"])
        assignment = self.get_object()

        part_transposition = assignment.part.transpositions.get(
            transposition=assignment.instrument.transposition
        )

        serializer = PartTranspositionSerializer(
            part_transposition, context=self.get_serializer_context()
        )
        return Response(serializer.data)

    def get_queryset(self):
        course = Course.objects.get(slug=self.kwargs["course_slug_slug"])
        role = self.request.user.enrollment_set.get(course=course).role

        if role.name == "Student":
            return Assignment.objects.filter(
                enrollment__course=course, enrollment__user=self.request.user
            ) #.select_related("activity", "instrument", "part", "part__piece")
        if role.name == "Teacher":
            return Assignment.objects.filter(enrollment__course=course).select_related("activity", "instrument", "part", "part__piece")
