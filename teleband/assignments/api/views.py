from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import AssignmentSerializer
from teleband.assignments.api.serializers import ActivitySerializer

from teleband.assignments.models import Assignment
from teleband.courses.models import Course


class AssignmentViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        course = Course.objects.get(slug=self.kwargs["course_slug_slug"])
        role = self.request.user.enrollment_set.get(course=course).role
        print("This user's role in this class is {}".format(role))

        if role.name == "Teacher":
            return ActivitySerializer
        return AssignmentSerializer

        return self.serializer_class

    def get_queryset(self):
        course = Course.objects.get(slug=self.kwargs["course_slug_slug"])
        role = self.request.user.enrollment_set.get(course=course).role

        if role.name == "Student":
            return Assignment.objects.filter(enrollment__course=course, enrollment__user=self.request.user)
        if role.name == "Teacher":
            # TODO this can't be right, front end should probably hit /course/:slug/activities for this info
            # Possibly /course/:slug/assignments should actually give activity -> student for each student
            return [
                a.activity
                for a in Assignment.objects.filter(course=course).distinct("activity")
            ]
