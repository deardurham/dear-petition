from rest_framework import serializers


class ValidationField(serializers.SerializerMethodField):
    def __init__(self, serializer, **kwargs):
        self.serializer_class = serializer
        super().__init__(**kwargs)

    def bind(self, field_name, parent):
        # The method name defaults to `get_{field_name}_data`
        if self.method_name is None:
            self.method_name = f"get_{field_name}_data"

        super().bind(field_name, parent)

        if self.serializer_class == self.parent:
            raise ValueError("Validation serializer must not be parent of this serializer field")

    def to_representation(self, value):
        # handle case where serializer is creating new value
        # TODO: Figure out how to get instance/native values for a new instance
        if not hasattr(value, "pk"):
            return None
        method = getattr(self.parent, self.method_name)
        try:
            data = method(value)
            self.serializer_class(data=data).is_valid(raise_exception=True)
            return {}
        except serializers.ValidationError as exc:
            return exc.detail
