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
        fields = ["id", "instrument", "external_id", "grade"]


class GenericNameSerializer(serializers.BaseSerializer):
    def __init__(self, *args, **kwargs):
        self.model_cls = kwargs.pop("model_cls", None)
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        return instance.name

    def to_internal_value(self, data):
        return self.model_cls.objects.get(name=data)
