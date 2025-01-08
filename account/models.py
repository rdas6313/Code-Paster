from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from .validators import validate_email


class UserManager(BaseUserManager):
    """ UserManager used as a manager to create new user object """

    def create_user(self, email, name, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        if not name:
            raise ValueError("Users must have a name")

        if not password:
            raise ValueError("Users must have password")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """ User class to hold user authentication information  """
    email = models.EmailField(
        max_length=255,
        unique=True,
        validators=[validate_email]
    )
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        """ return string representation """
        return str(self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
