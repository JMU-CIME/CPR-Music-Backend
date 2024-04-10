from rest_framework import serializers

from teleband.courses.models import Course, Enrollment
from teleband.instruments.api.serializers import InstrumentSerializer
from teleband.users.api.serializers import UserSerializer
from teleband.utils.serializers import GenericNameSerializer


class CourseRelatedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "start_date", "end_date", "url", "slug"]

        extra_kwargs = {
            "url": {"view_name": "api:course-detail", "lookup_field": "slug"},
        }


class CourseSerializer(CourseRelatedSerializer):
    owner = UserSerializer()

    class Meta(CourseRelatedSerializer.Meta):
        fields = CourseRelatedSerializer.Meta.fields + ["owner", "can_edit_instruments"]


class EnrollmentInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "instrument"]


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "user", "course", "instrument", "role"]


class EnrollmentSerializer(serializers.HyperlinkedModelSerializer):
    course = CourseSerializer()
    instrument = InstrumentSerializer()
    role = GenericNameSerializer()
    user = UserSerializer()

    class Meta:
        model = Enrollment
        fields = ["id", "course", "instrument", "role", "user"]

        extra_kwargs = {
            "course": {"view_name": "api:course-detail", "lookup_field": "slug"}
        }


class RosterSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    instrument = InstrumentSerializer()
    role = GenericNameSerializer()

    class Meta:
        model = Enrollment
        fields = ["id", "user", "instrument", "role"]
