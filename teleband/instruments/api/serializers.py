from rest_framework import serializers

from teleband.instruments.models import Instrument
from teleband.utils.serializers import GenericNameSerializer


class InstrumentSerializer(serializers.ModelSerializer):
    transposition = GenericNameSerializer()

    class Meta:
        model = Instrument
        fields = ["id", "name", "transposition"]
