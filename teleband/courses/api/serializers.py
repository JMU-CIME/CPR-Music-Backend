from rest_framework import serializers
from teleband.courses.models import Course


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        # fields = ["name", "owner", "users"]
        fields = ["name"]
