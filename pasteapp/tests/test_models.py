from pasteapp.models import *
from django.test import TestCase


class LanguageTestCase(TestCase):

    def test_language_creation(self):
        language = Language.objects.create(name="c++")
        self.assertIsInstance(language, Language)
        self.assertEqual(language.name, "c++")

    def test_language_name_length_constraints(self):
        name = "a" * 300
        with self.assertRaises(ValidationError):
            Language.objects.create(name=name)


class PasteTestCase(TestCase):

    def setUp(self):
        from datetime import timedelta
        from django.utils import timezone
        from django.contrib.auth import get_user_model
        self.user = get_user_model().objects.create_user(
            email="abc@abc.com", name="abc", password="1234")
        self.language = Language.objects.create(name="c++")
        self.expiry = timezone.now() + timedelta(days=1)

    def test_create_paste(self):

        paste = Paste.objects.create(
            code="abc",
            user=self.user,
            expired_at=self.expiry,
            language=self.language,

        )

        self.assertIsInstance(paste, Paste)
        self.assertEqual(paste.code, "abc")
        self.assertEqual(paste.expired_at, self.expiry)
        self.assertEqual(paste.user.id, self.user.id)
        self.assertEqual(paste.language.name, self.language.name)
        self.assertTrue(paste.sharable)
        self.assertFalse(paste.password)

    def test_create_paste_password_creation(self):
        paste = Paste.objects.create(
            code="abc",
            user=self.user,
            expired_at=self.expiry,
            language=self.language,

        )
        paste.create_password("1234")
        paste.save()
        self.assertTrue(paste.is_valid_password("1234"))
        paste = Paste.objects.get(pk=paste.id)
        self.assertTrue(paste.is_valid_password("1234"))

    def test_password_length_constraints(self):
        paste = Paste.objects.create(
            code="abc",
            user=self.user,
            expired_at=self.expiry,
            language=self.language,

        )
        password = "1" * 300
        paste.create_password(password)
        paste.save()
        self.assertTrue(paste.is_valid_password(password))

    def test_create_paste_foreign_key_constraints(self):
        from django.db.utils import IntegrityError
        
        with self.assertRaises(ValidationError):
            Paste.objects.create(
                code="abc",
                user_id=102,
                expired_at=self.expiry,
                language=self.language,

            )

        with self.assertRaises(ValidationError):
            Paste.objects.create(
                code="abc",
                user_id=self.user,
                expired_at=self.expiry,
                language_id=50,

            )

    def test_checking_modified_created_at(self):
        paste = Paste.objects.create(
            code="abc",
            user=self.user,
            expired_at=self.expiry,
            language=self.language,

        )
        created_at = paste.created_at
        paste.create_password("113")
        paste.save()
        self.assertEqual(created_at, paste.created_at)

    def test_paste_deletion_on_delete_language(self):
        Paste.objects.create(
            code="abc",
            user=self.user,
            expired_at=self.expiry,
            language=self.language,

        )
        self.language.delete()
        self.assertEqual(Paste.objects.all().count(), 0)

    def test_paste_deletion_on_delete_user(self):
        Paste.objects.create(
            code="abc",
            user=self.user,
            expired_at=self.expiry,
            language=self.language,

        )
        self.user.delete()
        self.assertEqual(Paste.objects.all().count(), 0)
