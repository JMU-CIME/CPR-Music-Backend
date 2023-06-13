from rest_framework import serializers

from teleband.assignments.models import Assignment, Activity, ActivityType
from teleband.courses.api.serializers import EnrollmentSerializer
from teleband.instruments.api.serializers import InstrumentSerializer
from teleband.submissions.api.serializers import SubmissionSerializer
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
    enrollment = EnrollmentSerializer()
    submissions = SubmissionSerializer(many=True)

    class Meta:
        model = Assignment
        # fields = ["activity", "deadline", "instrument", "id", "url"]
        fields = ["activity", "deadline", "instrument", "part", "id", "enrollment", "submissions"]

        extra_kwargs = {
            "url": {"view_name": "api:assignment-detail", "lookup_field": "id"},
        }



class AssignmentViewSetSerializer(serializers.ModelSerializer):
    activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all())
    activity_type_name = serializers.CharField(source="activity.activity_type.name", read_only=True)
    activity_type_category = serializers.CharField(source="activity.activity_type.category.name", read_only=True)
    part_type = serializers.CharField(source="activity.part_type.name", read_only=True)
    piece_name = serializers.SlugField(source="part.piece.name", read_only=True)
    piece_id = serializers.IntegerField(source="part.piece.id", read_only=True)
    piece_slug = serializers.SlugField(source="part.piece.slug", read_only=True)
    instrument = serializers.CharField(source="instrument.name", read_only=True)
    transposition = serializers.CharField(source="instrument.transposition.name", read_only=True)
    # instrument = InstrumentSerializer()
    # part = PartSerializer()
    # enrollment = EnrollmentSerializer()
    # submissions = SubmissionSerializer(many=True)

    class Meta:
        model = Assignment
        # fields = ["activity", "deadline", "instrument", "id", "url"]
        # fields = ["activity", "deadline", "instrument", "part", "id", "enrollment", "submissions"]
        fields = ["id", "activity", "activity_type_name", "activity_type_category", "part_type",
                  "piece_name", "piece_id", "piece_slug", "instrument", "transposition"]

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
