from typing import Any, Iterable
from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.utils import timezone


class ObjectManager(models.Manager):
    """ helps to create object and manage them """

    def create(self, **kwargs: Any) -> Any:
        """ overriding create method to create a instance and enforced validation """
        instance = self.model(**kwargs)
        if isinstance(instance, Language):
            instance.full_clean()
        instance.save()
        return instance


class Language(models.Model):
    """ This model holds programming language related data """
    name = models.CharField(max_length=255)
    objects = ObjectManager()


class Paste(models.Model):
    """ This model is responsible for holding paste related data """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.TextField()
    created_at = models.DateTimeField()
    sharable = models.BooleanField(default=True)
    password = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    expired_at = models.DateTimeField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    objects = ObjectManager()

    def create_password(self, password):
        """ use to create password for the paste """
        self.password = make_password(password)

    def is_valid_password(self, password):
        """ use to check if a password is valid or not """
        return check_password(password, self.password)

    def clean(self):
        """ use for validation """
        super().clean()
        if self.expired_at < self.created_at:
            raise ValidationError(
                "Expiry date can not be smaller than the created date! ")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """ use to save the paste to database """
        if not self.created_at:
            self.created_at = timezone.now()
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)
