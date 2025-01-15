from rest_framework import serializers
from .models import Paste
from django.core.exceptions import ValidationError


class PasteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=False, trim_whitespace=False, write_only=True)
    sharable = serializers.BooleanField(required=False, default=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Paste
        fields = ['id', 'code', 'sharable',
                  'password', 'expired_at', 'language', 'user']

    def save(self, **kwargs):
        self.validated_data['user'] = self.context.get('user', None)
        password = self.validated_data.pop('password', None)
        paste = self.save_to_database(**kwargs)
        if password:
            paste.create_password(password)
            paste.save()
        return paste

    def save_to_database(self, **kwargs):
        try:
            paste = super().save(**kwargs)
        except ValidationError as e:
            errors = {'field': e.messages}
            raise serializers.ValidationError(errors, code='invalid_input')
        else:
            return paste


class SinglePastePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(trim_whitespace=False, write_only=True)
