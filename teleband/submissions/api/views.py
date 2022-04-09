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
        if "piece_slug" not in request.GET or "activity_name" not in request.GET:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "error": "Missing piece_slug or activity_name (figure it out!) in get data"
                },
            )
        
        course_id = self.kwargs["course_slug_slug"]
        piece_slug = request.GET["piece_slug"]
        activity_name = request.GET["activity_name"]
        
        queryset =  (
            Submission.objects.filter(
                assignment__enrollment__course__slug=course_id,
                assignment__activity__activity_type__name=activity_name,
                assignment__part__piece__slug=piece_slug,
            )
            .order_by("assignment__enrollment", "-submitted")
            .distinct("assignment__enrollment")
        )

        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)
