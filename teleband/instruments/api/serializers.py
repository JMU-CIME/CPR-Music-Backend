from rest_framework import serializers

from teleband.instruments.models import Instrument


class TranspositionSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return instance.name


class InstrumentSerializer(serializers.ModelSerializer):
    transposition = TranspositionSerializer()

    class Meta:
        model = Instrument
        fields = ["id", "name", "transposition"]
