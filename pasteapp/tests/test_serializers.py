from rest_framework.test import APITransactionTestCase
from pasteapp.serializers import *
from pasteapp.models import *


class PasteSerializerTestCase(APITransactionTestCase):

    def setUp(self):
        self.language = Language.objects.create(name='python')

    def tearDown(self):
        Language.objects.filter(id=self.language.id).delete()

    def test_serializer_validation(self):
        data = {
            'code': 'abc',
            'sharable': True,
            'password': '123',
            'expired_at': '2025-10-25 14:30:59',
            'language': self.language.id
        }

        serializer = PasteSerializer(data=data)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        paste = serializer.save()
        self.assertIsInstance(paste, Paste)
        self.assertTrue(paste.id)
        self.assertEqual(paste.code, data['code'])
        self.assertEqual(paste.sharable, data['sharable'])
        self.assertTrue(paste.is_valid_password(data['password']))
        self.assertEqual(paste.expired_at.strftime(
            '%Y-%m-%d %H:%M:%S'), data['expired_at'])
        self.assertEqual(paste.language.id, data['language'])

    def test_serializer_validation_with_nopassword_nosharable(self):

        data = {
            'code': 'abc',
            'expired_at': '2025-10-25 14:30:59',
            'language': self.language.id
        }

        serializer = PasteSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        paste = serializer.save()
        self.assertIsInstance(paste, Paste)
        self.assertEqual(paste.code, data['code'])
        self.assertTrue(paste.sharable)
        self.assertEqual(paste.password, '')
        self.assertEqual(paste.expired_at.strftime(
            '%Y-%m-%d %H:%M:%S'), data['expired_at'])
        self.assertEqual(paste.language.id, data['language'])

    def test_serializer_validation_with_nopassword(self):
        data = {
            'code': 'abc',
            'sharable': False,
            'expired_at': '2025-10-25 14:30:59',
            'language': self.language.id
        }
        serializer = PasteSerializer(data=data)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        paste = serializer.save()
        self.assertIsInstance(paste, Paste)
        self.assertEqual(paste.code, data['code'])
        self.assertEqual(paste.sharable, data['sharable'])
        self.assertEqual(paste.password, '')
        self.assertEqual(paste.expired_at.strftime(
            '%Y-%m-%d %H:%M:%S'), data['expired_at'])
        self.assertEqual(paste.language.id, data['language'])

    def test_serializer_missing_field_code(self):
        data = {
            'expired_at': '2025-10-25 14:30:59',
            'language': self.language.id
        }

        serializer = PasteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('code' in serializer.errors)

    def test_serializer_missing_field_expired_at(self):
        data = {
            'code': 'abc',
            'language': self.language.id
        }

        serializer = PasteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('expired_at' in serializer.errors)

    def test_serializer_missing_field_language(self):
        data = {
            'code': 'abc',
            'expired_at': '2025-10-25 14:30:59',
        }

        serializer = PasteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('language' in serializer.errors)

    def test_serializer_missing_fields(self):

        serializer = PasteSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertTrue('language' in serializer.errors)
        self.assertTrue('expired_at' in serializer.errors)
        self.assertTrue('code' in serializer.errors)

    def test_serializer_password_write_only(self):
        data = {
            'code': 'abc',
            'sharable': True,
            'password': '123',
            'expired_at': '2025-10-25 14:30:59',
            'language': self.language.id
        }

        serializer = PasteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse('password' in serializer.data)

    def test_serializer_not_trim_whitespace(self):
        data = {
            'code': 'abc',
            'sharable': True,
            'password': ' 123 ',
            'expired_at': '2025-10-25 14:30:59',
            'language': self.language.id
        }

        serializer = PasteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        paste = serializer.save()
        self.assertTrue(paste.is_valid_password(data['password']))

    def test_serializer_responses(self):
        data = {
            'code': 'abc',
            'sharable': False,
            'password': ' 123 ',
            'expired_at': '2025-10-25 14:30:59',
            'language': self.language.id
        }

        serializer = PasteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertTrue('id' in serializer.data)
        self.assertTrue('code' in serializer.data)
        self.assertTrue('sharable' in serializer.data)
        self.assertTrue('expired_at' in serializer.data)
        self.assertTrue('language' in serializer.data)
        self.assertTrue('password' not in serializer.data)

    def test_serializer_responses_missing_sharable(self):
        data = {
            'code': 'abc',
            'password': ' 123 ',
            'expired_at': '2025-10-25 14:30:59',
            'language': self.language.id
        }

        serializer = PasteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertTrue('code' in serializer.data)
        self.assertTrue('sharable' in serializer.data)
        self.assertTrue('expired_at' in serializer.data)
        self.assertTrue('language' in serializer.data)
        self.assertTrue('password' not in serializer.data)

    def test_serializer_updation(self):
        from datetime import timedelta
        from django.utils import timezone
        paste = Paste.objects.create(
            code='abc',
            sharable=False,
            expired_at=timezone.now() + timedelta(days=1),
            language=self.language
        )

        data = {
            'code': 'def',
            'sharable': True,
            'password': '123',
            'expired_at': '2026-10-25 14:30:59',
            'language': self.language.id
        }

        serializer = PasteSerializer(paste, data=data)
        self.assertTrue(serializer.is_valid())
        old_paste = paste
        paste = serializer.save()
        self.assertIsInstance(paste, Paste)
        self.assertEqual(old_paste.id, paste.id)
        self.assertEqual(paste.code, data['code'])
        self.assertEqual(paste.sharable, data['sharable'])
        self.assertTrue(paste.is_valid_password(data['password']))
        self.assertEqual(paste.expired_at.strftime(
            '%Y-%m-%d %H:%M:%S'), data['expired_at'])
        self.assertEqual(paste.language.id, data['language'])

    def test_serializer_updation_partially(self):
        from datetime import timedelta
        from django.utils import timezone
        expiry = timezone.now() + timedelta(days=1)
        paste = Paste.objects.create(
            code='abc',
            sharable=False,
            expired_at=expiry,
            language=self.language
        )

        data = {
            'code': 'abc',
            'sharable': False,
            'password': '123',
            'expired_at': expiry.strftime(
                '%Y-%m-%d %H:%M:%S'),
            'language': self.language.id
        }

        serializer = PasteSerializer(
            paste, data={'password': data['password']}, partial=True)
        self.assertTrue(serializer.is_valid())
        old_paste = paste
        paste = serializer.save()
        self.assertIsInstance(paste, Paste)
        self.assertEqual(old_paste.id, paste.id)
        self.assertEqual(paste.code, data['code'])
        self.assertEqual(paste.sharable, data['sharable'])
        self.assertTrue(paste.is_valid_password(data['password']))
        self.assertEqual(paste.expired_at.strftime(
            '%Y-%m-%d %H:%M:%S'), data['expired_at'])
        self.assertEqual(paste.language.id, data['language'])
