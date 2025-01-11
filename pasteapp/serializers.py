from rest_framework import serializers
from .models import Paste


class PasteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=False, trim_whitespace=False, write_only=True)
    sharable = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = Paste
        fields = ['code', 'sharable', 'password', 'expired_at', 'language']

    def save(self, **kwargs):
        password = self.validated_data.pop('password', None)
        paste = super().save(**kwargs)
        if password:
            paste.create_password(password)
        return paste
