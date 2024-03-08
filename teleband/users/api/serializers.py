from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from teleband.instruments.api.serializers import InstrumentSerializer
from teleband.utils.serializers import GenericNameSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    instrument = InstrumentSerializer
    # groups = [g for g in groups.values()]
    groups = GenericNameSerializer(model_cls=Group, many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "url",
            "grade",
            "instrument",
            "external_id",
            "groups",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class UserInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "instrument", "external_id", "grade"]
