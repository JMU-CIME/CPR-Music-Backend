from rest_framework import serializers

from teleband.assignments.models import Assignment, Activity
from teleband.instruments.api.serializers import InstrumentSerializer
from teleband.users.api.serializers import GenericNameSerializer
from teleband.musics.api.serializers import PartTranspositionSerializer


class ActivitySerializer(serializers.ModelSerializer):
    activity_type = GenericNameSerializer()
    part = PartTranspositionSerializer()

    class Meta:
        model = Activity
        fields = ["activity_type", "part", "body"]


class AssignmentSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()
    instrument = InstrumentSerializer()

    class Meta:
        model = Assignment
        # fields = ["activity", "deadline", "instrument", "url"]
        fields = ["activity", "deadline", "instrument", "id", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:assignment-detail", "lookup_field": "id"},
        }
