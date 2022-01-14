from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import PieceSerializer
from teleband.musics.models import Piece


class PieceViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = PieceSerializer
    queryset = Piece.objects.all()
    # permission_classes = [IsTeacher]
