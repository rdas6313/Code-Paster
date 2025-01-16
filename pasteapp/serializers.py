from rest_framework import serializers
from .models import Paste
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from datetime import datetime


class PasteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=False, trim_whitespace=False, write_only=True)
    sharable = serializers.BooleanField(required=False, default=True)
    id = serializers.UUIDField(read_only=True)
    password_protected = serializers.SerializerMethodField()

    class Meta:
        model = Paste
        fields = ['id', 'code', 'sharable', 'password_protected',
                  'password', 'expired_at', 'language', 'user']

    def get_password_protected(self, paste):
        return bool(paste.password)

    def validate_expired_at(self, expiry_date):
        creation_date = timezone.now()
        if not self.context.get('user', None) and expiry_date - creation_date > settings.GUEST_PASTE_MAX_VALIDITY:
            raise serializers.ValidationError(
                detail=f'Unauthenticated user can\'t have paste expiry more than {
                    settings.GUEST_PASTE_MAX_VALIDITY.days
                } days'
            )
        if expiry_date < creation_date:
            raise serializers.ValidationError(
                detail='Paste expiry can\'t be smaller than creation which is current date and time')
        return expiry_date

    def validate_sharable(self, sharable):
        if not self.context.get('user', None) and not sharable:
            raise serializers.ValidationError(
                detail='Unauthenticated user can\'t have unsharable data')
        return sharable

    def validate_password(self, password):
        if not self.context.get('user', None) and password:
            raise serializers.ValidationError(
                detail='Unauthenticated user can\'t have password protected data')
        return password

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
