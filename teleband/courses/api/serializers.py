from rest_framework import serializers

from teleband.courses.models import Course, Enrollment
from teleband.instruments.api.serializers import InstrumentSerializer
from teleband.users.api.serializers import GenericNameSerializer, UserSerializer


class CourseRelatedSerializer(serializers.HyperlinkedModelSerializer):
    # assignments = serializers.HyperlinkedIdentityField(view_name="api:assignment-list")

    class Meta:
        model = Course
        fields = ["name", "owner", "start_date", "end_date", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:course-detail", "lookup_field": "slug"},
            "owner": {"view_name": "api:user-detail", "lookup_field": "username"},
            # "assignments": {"view_name": "api:assignment-list", "lookup_field": "slug"}
        }


class CourseSerializer(CourseRelatedSerializer):
    owner = UserSerializer()


class EnrollmentSerializer(serializers.HyperlinkedModelSerializer):
    course = CourseSerializer()
    instrument = InstrumentSerializer()
    role = GenericNameSerializer()

    class Meta:
        model = Enrollment
        fields = ["course", "instrument", "role"]

        extra_kwargs = {
            "course": {"view_name": "api:course-detail", "lookup_field": "slug"}
        }
