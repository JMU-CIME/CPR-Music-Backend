from rest_framework import serializers

from teleband.musics.models import Piece, Part, PartTransposition, Composer

from teleband.musics.models import PartTransposition
from teleband.users.api.serializers import GenericNameSerializer


class ComposerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composer
        fields = ["name", "url"]


class PieceSerializer(serializers.ModelSerializer):
    composer = ComposerSerializer()

    class Meta:
        model = Piece
        fields = [
            "name",
            "composer",
            "video",
            "audio",
            "date_composed",
            "ensemble_type",
        ]


class PartSerializer(serializers.ModelSerializer):
    piece = PieceSerializer()

    class Meta:
        model = Part
        fields = ["name", "piece"]


class PartTranspositionSerializer(serializers.ModelSerializer):
    part = PartSerializer()
    transposition = GenericNameSerializer()

    class Meta:
        model = PartTransposition
        fields = ["part", "transposition", "notation"]
