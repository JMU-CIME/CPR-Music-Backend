from rest_framework import serializers

from teleband.assignments.models import Assignment, Activity, ActivityType
from teleband.instruments.api.serializers import InstrumentSerializer
from teleband.utils.serializers import GenericNameSerializer
from teleband.musics.api.serializers import PartTranspositionSerializer, PartSerializer


class ActivityTypeSerializer(serializers.ModelSerializer):
    category = GenericNameSerializer()

    class Meta:
        model = ActivityType
        fields = ["name", "category"]


class ActivitySerializer(serializers.ModelSerializer):
    activity_type = ActivityTypeSerializer()
    part_type = GenericNameSerializer()

    class Meta:
        model = Activity
        fields = ["activity_type", "part_type", "body"]


class AssignmentSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()
    instrument = InstrumentSerializer()
    part = PartSerializer()

    class Meta:
        model = Assignment
        # fields = ["activity", "deadline", "instrument", "id", "url"]
        fields = ["activity", "deadline", "instrument", "part", "id"]

        extra_kwargs = {
            "url": {"view_name": "api:assignment-detail", "lookup_field": "id"},
        }


class AssignmentInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ["id", "instrument"]


class NotationAssignmentSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()
    instrument = InstrumentSerializer()
    part = PartSerializer()

    class Meta:
        model = Assignment
        # fields = ["activity", "deadline", "instrument", "id", "url"]
        fields = ["activity", "deadline", "instrument", "part", "id"]

        extra_kwargs = {
            "url": {"view_name": "api:assignment-detail", "lookup_field": "id"},
        }
