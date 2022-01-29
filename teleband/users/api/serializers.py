from django.contrib.auth import get_user_model
from rest_framework import serializers

from teleband.instruments.api.serializers import InstrumentSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    instrument = InstrumentSerializer

    class Meta:
        model = User
        fields = ["id", "username", "name", "url", "grade", "instrument", "external_id"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class UserInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "instrument", "external_id", "grade"]
