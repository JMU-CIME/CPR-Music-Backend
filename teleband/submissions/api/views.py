from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import (
    SubmissionSerializer,
    SubmissionCreateSerializer,
    AttachmentSerializer,
    AttachmentCreateSerializer,
)

from teleband.courses.models import Course
from teleband.submissions.models import Submission, SubmissionAttachment
from teleband.assignments.models import Assignment


class SubmissionViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SubmissionCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        print("SubmissionViewSet kwargs {}".format(self.kwargs))
        return self.queryset.filter(assignment_id=self.kwargs["assignment_id"])

    def perform_create(self, serializer):
        serializer.save(
            assignment=Assignment.objects.get(pk=self.kwargs["assignment_id"])
        )


class AttachmentViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    serializer_class = AttachmentSerializer
    queryset = SubmissionAttachment.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AttachmentCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        print("AttachmentViewSet kwargs {}".format(self.kwargs))
        return self.queryset.filter(submission_id=self.kwargs["submission_pk"])

    def perform_create(self, serializer):
        serializer.save(
            submission=Submission.objects.get(pk=self.kwargs["submission_pk"])
        )
