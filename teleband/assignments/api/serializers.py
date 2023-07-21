from rest_framework import serializers

from teleband.assignments.models import Assignment, Activity, ActivityType, AssignmentGroup, PiecePlan
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


class GroupSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True)
    members = serializers.SerializerMethodField(method_name="get_members")

    def get_members(self, obj):
        assignments = Assignment.objects.filter(group=obj)
        assignment_enrollments = [(a, a.enrollment) for a in assignments]
        member_list = [{"enrollment_id": ae[1].id, 
                        "enrollment_username": ae[1].user.username, 
                        "activity_type_name": ae[0].activity.activity_type_name, 
                        "assignment_submitted": bool(ae[0].submissions.count())} for ae in assignment_enrollments]
        return member_list

    class Meta:
        model = AssignmentGroup
        fields = ["type", "members"]


class AssignmentSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()
    instrument = InstrumentSerializer()
    part = PartSerializer()
    enrollment = EnrollmentSerializer()
    submissions = SubmissionSerializer(many=True)

    class Meta:
        model = Assignment
        # fields = ["activity", "deadline", "instrument", "id", "url"]
        fields = ["activity", "deadline", "instrument", "part", "id", "enrollment", "submissions", "group"]

        extra_kwargs = {
            "url": {"view_name": "api:assignment-detail", "lookup_field": "id"},
        }

    # def get_fields(self):
    #     fields = super().get_fields()
    #     if not self.instance.group: 
    #         del fields['group']
    #     return fields 



class AssignmentViewSetSerializer(serializers.ModelSerializer):
    activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all())
    activity_type_name = serializers.CharField(source="activity.activity_type_name", read_only=True)
    activity_type_category = serializers.CharField(source="activity.category", read_only=True)
    part_type = serializers.CharField(source="activity.part_type.name", read_only=True)
    piece_name = serializers.SlugField(source="piece.name", read_only=True)
    piece_id = serializers.IntegerField(source="piece.id", read_only=True)
    piece_slug = serializers.SlugField(source="piece.slug", read_only=True)
    instrument = serializers.CharField(source="instrument.name", read_only=True)
    transposition = serializers.CharField(source="instrument.transposition.name", read_only=True)
    group = GroupSerializer()
    # instrument = InstrumentSerializer()
    # part = PartSerializer()
    # enrollment = EnrollmentSerializer()
    # submissions = SubmissionSerializer(many=True)

    class Meta:
        model = Assignment
        # fields = ["activity", "deadline", "instrument", "id", "url"]
        # fields = ["activity", "deadline", "instrument", "part", "id", "enrollment", "submissions"]
        fields = ["id", "activity", "activity_type_name", "activity_type_category", "part_type",
                  "piece_name", "piece_id", "piece_slug", "instrument", "transposition", "group"]

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

class PiecePlanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    type = serializers.CharField()
    piece = serializers.SlugRelatedField(slug_field="name", read_only=True)
    activities = ActivitySerializer(many=True)

    class Meta:
        model = PiecePlan
        fields = ["id", "piece", "type", "activities"]

        # extra_kwargs = {
        #     "url": {"view_name": "api:pieceplan-detail", "lookup_field": "id"},
        # }