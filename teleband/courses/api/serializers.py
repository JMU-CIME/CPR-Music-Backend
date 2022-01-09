from rest_framework import serializers

from teleband.courses.models import Course, Enrollment
from teleband.instruments.api.serializers import InstrumentSerializer
from teleband.users.api.serializers import RoleSerializer

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["name", "slug"]


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    instrument = InstrumentSerializer()
    role = RoleSerializer()

    class Meta:
        model = Enrollment
        fields = ["course", "instrument", "role"]

