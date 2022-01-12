from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import EnrollmentSerializer, CourseSerializer, CourseRelatedSerializer

from teleband.courses.models import Enrollment, Course
from teleband.assignments.models import Assignment
from teleband.assignments.api.serializers import AssignmentSerializer


class EnrollmentViewSet(ListModelMixin, GenericViewSet):
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

    @action(detail=True)
    def assignments(self, request, **kwargs):
        queryset = Assignment.objects.filter(
            user=request.user, course=self.get_object()
        )
        serializer = AssignmentSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)
