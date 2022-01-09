from rest_framework import serializers

from teleband.courses.models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["course", "instrument", "role"]
