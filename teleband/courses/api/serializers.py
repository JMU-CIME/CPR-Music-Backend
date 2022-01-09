from rest_framework import serializers

from teleband.courses.models import Course, Enrollment
from teleband.instruments.api.serializers import InstrumentSerializer
from teleband.users.api.serializers import RoleSerializer, UserSerializer


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Course
        fields = ["name", "owner", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:course-detail", "lookup_field": "slug"},
            "owner": {"view_name": "api:user-detail", "lookup_field": "username"},
        }


class EnrollmentSerializer(serializers.HyperlinkedModelSerializer):
    course = CourseSerializer()
    instrument = InstrumentSerializer()
    role = RoleSerializer()

    class Meta:
        model = Enrollment
        fields = ["course", "instrument", "role"]

        extra_kwargs = {
            "course": {"view_name": "api:course-detail", "lookup_field": "slug"}
        }
