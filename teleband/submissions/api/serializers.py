from rest_framework import serializers

from teleband.submissions.models import Grade, Submission, SubmissionAttachment
# from teleband.assignments.api.serializers import AssignmentSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["id", "submitted", "content", "grade", "self_grade"]

        # extra_kwargs = {
        #     "assignment": {"view_name": "api:assignment-detail", "lookup_field": "id"},
        # }


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionAttachment
        fields = ["id", "file", "submitted"]

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ["id", "rhythm", "tone", "expression", "created_at", "grader", "student_submission", "own_submission"]

