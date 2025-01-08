from django.core.exceptions import ValidationError
import re


def validate_email(value):
    """ Validators to validate email """
    pattern = ".+@.+\..+"
    if not re.search(pattern, value):
        raise ValidationError("Invalid email!")
