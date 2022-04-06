from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


from .serializers import (
    SubmissionSerializer,
    AttachmentSerializer,
    TeacherSubmissionSerializer,
)

from teleband.courses.models import Course
from teleband.submissions.models import Submission, SubmissionAttachment
from teleband.assignments.models import Assignment


class SubmissionViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def get_queryset(self):
        return self.queryset.filter(assignment_id=self.kwargs["assignment_id"])

    def perform_create(self, serializer):
        serializer.save(
            assignment=Assignment.objects.get(pk=self.kwargs["assignment_id"])
        )

    # @action(detail=False)
    # def get_


class AttachmentViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    serializer_class = AttachmentSerializer
    queryset = SubmissionAttachment.objects.all()

    def get_queryset(self):
        return self.queryset.filter(submission_id=self.kwargs["submission_pk"])

    def perform_create(self, serializer):
        serializer.save(
            submission=Submission.objects.get(pk=self.kwargs["submission_pk"])
        )


class TeacherSubmissionViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = TeacherSubmissionSerializer
    queryset = Submission.objects.all()

    # def get_queryset(self,):
    #     pass

    @action(detail=False)
    def recent(self, request, **kwargs):
        if "piece_id" not in request.GET or "activity_id" not in request.GET:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "error": "Missing piece_id or activity_id (figure it out!) in get data"
                },
            )
        
        course_id = self.kwargs["course_slug_slug"]
        piece_id = request.GET["piece_id"]
        activity_id = request.GET["activity_id"]
        
        queryset =  (
            Submission.objects.filter(
                assignment__enrollment__course__slug=course_id,
                assignment__activity__activity_type=activity_id,
                assignment__part__piece_id=piece_id,
            )
            .order_by("assignment__enrollment", "-submitted")
            .distinct("assignment__enrollment")
        )

        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)
