from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from teleband.instruments.models import Instrument, Transposition


class TranspositionFactory(DjangoModelFactory):

    name = Faker("color")

    class Meta:
        model = Transposition


class InstrumentFactory(DjangoModelFactory):

    name = Faker("color")
    transposition = SubFactory(TranspositionFactory)

    class Meta:
        model = Instrument
