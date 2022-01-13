from rest_framework import serializers

from teleband.submissions.models import Submission, SubmissionAttachment
from teleband.assignments.api.serializers import AssignmentSerializer


class AttachmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionAttachment
        fields = ["id", "file", "submitted"]


class SubmissionSerializer(serializers.ModelSerializer):
    assignment = AssignmentSerializer()
    attachments = AttachmentCreateSerializer(many=True)

    class Meta:
        model = Submission
        fields = ["id", "assignment", "submitted", "content", "attachments"]

        # extra_kwargs = {
        #     "assignment": {"view_name": "api:assignment-detail", "lookup_field": "id"},
        # }


class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["content"]


class AttachmentSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer()

    class Meta:
        model = SubmissionAttachment
        fields = ["submission", "file", "submitted"]
