from django.test import TestCase
from account.models import *
from django.core.exceptions import ValidationError


class UserTestCase(TestCase):

    def test_user_creation(self):
        user = User.objects.create_user(
            email="test@test.com",
            name="Test",
            password="1234"
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.name, "Test")
        self.assertTrue(user.check_password("1234"))
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)

    def test_user_email_length_constraints(self):
        email = "abc@abc.com" + ("a" * 255)
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email=email,
                name="Test",
                password="1234"
            )

    def test_user_name_length_constraints(self):
        name = "a" * 256
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email="abc@abc.com",
                name=name,
                password="1234"
            )

    def test_user_creation_unique_constraints(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email="test@test.com",
                name="Test",
                password="1234"
            )
            User.objects.create_user(
                email="test@test.com",
                name="Test",
                password="1234"
            )

    def test_user_creation_with_missing_value(self):
        with self.assertRaises(TypeError):
            user = User.objects.create_user(
                name="Test",
                password="1234"
            )
        with self.assertRaises(ValueError):
            user = User.objects.create_user(
                email=None,
                name="Test",
                password="1234"
            )
        with self.assertRaises(ValueError):
            user = User.objects.create_user(
                email="",
                name="Test",
                password="1234"
            )
        with self.assertRaises(ValueError):
            user = User.objects.create_user(
                email="abc@abc.com",
                name="",
                password="1234"
            )
        with self.assertRaises(ValueError):
            user = User.objects.create_user(
                email="abc@abc.com",
                name="Raja",
                password=None
            )
        with self.assertRaises(ValueError):
            user = User.objects.create_user(
                email="abc@abc.com",
                name="Raja",
                password=""
            )

    def test_user_creation_wrong_email(self):

        with self.assertRaises(ValidationError):
            user = User.objects.create_user(
                email="test.com",
                name="Test",
                password="1234"
            )
        with self.assertRaises(ValidationError):
            user = User.objects.create_user(
                email="@test.com",
                name="Test",
                password="1234"
            )
        with self.assertRaises(ValidationError):
            user = User.objects.create_user(
                email="abc@.com",
                name="Test",
                password="1234"
            )
        with self.assertRaises(ValidationError):
            user = User.objects.create_user(
                email="abc@testcom",
                name="Test",
                password="1234"
            )

    def test_create_super_user(self):
        user = User.objects.create_superuser(
            email="abc@abc.com",
            name="Raja",
            password="1234"
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "abc@abc.com")
        self.assertEqual(user.name, "Raja")
        self.assertTrue(user.check_password("1234"))
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser_with_less_argument(self):
        with self.assertRaises(TypeError):
            user = User.objects.create_superuser(
                name="Raja",
                password="1234"
            )

    def test_create_superuser_with_wrong_value(self):
        with self.assertRaises(ValueError):
            user = User.objects.create_superuser(
                email=None,
                name="Test",
                password="1234"
            )
        with self.assertRaises(ValueError):
            user = User.objects.create_superuser(
                email="",
                name="Test",
                password="1234"
            )
        with self.assertRaises(ValueError):
            user = User.objects.create_superuser(
                email="abc@abc.com",
                name="",
                password="1234"
            )
        with self.assertRaises(ValueError):
            user = User.objects.create_superuser(
                email="abc@abc.com",
                name="Raja",
                password=None
            )
        with self.assertRaises(ValueError):
            user = User.objects.create_superuser(
                email="abc@abc.com",
                name="Raja",
                password=""
            )
