from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import PieceSerializer, PieceCreateSerializer
from teleband.musics.models import Piece


class PieceViewSet(
    RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet
):
    serializer_class = PieceSerializer
    queryset = Piece.objects.all()
    # permission_classes = [IsTeacher]

    def get_serializer_class(self):
        if self.action == "create":
            return PieceCreateSerializer
        return self.serializer_class
