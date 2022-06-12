from rest_framework import serializers
from teleband.submissions.api.serializers import AttachmentSerializer, GradeSerializer
from teleband.assignments.api.serializers import AssignmentSerializer
from teleband.submissions.models import Submission


class TeacherSubmissionSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(read_only=True, many=True)
    assignment = AssignmentSerializer()
    grade = GradeSerializer()
    self_grade = GradeSerializer()

    def get_attachments(self, queryset):
        print(queryset)
        return None

    class Meta:
        model = Submission
        fields = [
            "id",
            "assignment",
            "submitted",
            "content",
            "attachments",
            "grade",
            "self_grade",
        ]

        # extra_kwargs = {
        #     "assignment": {"view_name": "api:assignment-detail", "lookup_field": "id"},
        # }
