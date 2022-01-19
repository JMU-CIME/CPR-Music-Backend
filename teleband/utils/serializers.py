from rest_framework import serializers


class GenericNameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        self.model_cls = kwargs.pop("model_cls", None)
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        return instance.name

    def to_internal_value(self, data):
        return self.model_cls.objects.get(name=data)
