from django.db.models import query
from rest_framework import viewsets
from teleband.courses.models import Course
from .serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Course.objects.filter(owner=user)
        return queryset
