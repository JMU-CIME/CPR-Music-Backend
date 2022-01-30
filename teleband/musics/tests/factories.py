from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from teleband.musics.models import EnsembleType, Piece


class EnsembleTypeFactory(DjangoModelFactory):

    name = Faker("color")

    class Meta:
        model = EnsembleType


class PieceFactory(DjangoModelFactory):

    name = Faker("name")
    ensemble_type = SubFactory(EnsembleTypeFactory)

    class Meta:
        model = Piece
