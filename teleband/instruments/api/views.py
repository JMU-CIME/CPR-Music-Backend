from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import InstrumentSerializer
from teleband.instruments.models import Instrument


class InstrumentViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = InstrumentSerializer
    queryset = Instrument.objects.all()
    lookup_field = "id"
