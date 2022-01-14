from rest_framework import serializers

from teleband.submissions.models import Submission, SubmissionAttachment
from teleband.assignments.api.serializers import AssignmentSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["id", "submitted", "content"]

        # extra_kwargs = {
        #     "assignment": {"view_name": "api:assignment-detail", "lookup_field": "id"},
        # }


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionAttachment
        fields = ["id", "file", "submitted"]
