from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class GenericNameSerializer(serializers.BaseSerializer):
    def __init__(self, *args, **kwargs):
        self.model_cls = kwargs.pop("model_cls", None)
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        return instance.name

    def to_internal_value(self, data):
        return self.model_cls.objects.get(name=data)
