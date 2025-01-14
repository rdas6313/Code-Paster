from rest_framework.test import APITestCase
from django.urls import reverse
from pasteapp.models import *
from rest_framework import status


class PasteViewSetTestcase(APITestCase):

    def setUp(self):
        self.language = Language.objects.create(name='python')
        self.user = get_user_model().objects.create_user(
            email="test123@test123.com", name="Test name", password="123")
        self.user.is_active = True
        self.user.save()

    def tearDown(self):
        Language.objects.all().delete()
        self.user.delete()

    def test_paste_create_as_guest(self):
        url = reverse('paste-list')
        data = {
            'code': 'test',
            'expired_at': '2026-12-12 11:00',
            'language': self.language.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in data.items():
            if key == 'expired_at':
                continue
            self.assertEqual(response.data.get(key, None), value)
        self.assertTrue(response.data.get('sharable', False))
        self.assertTrue('password' not in response.data)
        self.assertIsNone(response.data.get('user', None))

    def test_paste_create_as_user(self):
        url = reverse('paste-list')
        data = {
            'code': 'test2',
            'expired_at': '2026-12-12 11:00',
            'sharable': False,
            'language': self.language.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in data.items():
            if key == 'expired_at':
                continue
            self.assertEqual(response.data.get(key, None), value)
        self.assertFalse(response.data.get('sharable', False))
        self.assertTrue('password' not in response.data)
        self.assertEqual(response.data.get('user', None), self.user.id)

    def test_paste_list_for_guest_user(self):
        self.test_paste_create_as_guest()
        self.test_paste_create_as_user()
        url = reverse('paste-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for data in response.data:
            self.assertTrue(data.get('sharable', False))
        self.assertEqual(len(response.data), 1)

    def test_paste_list_for_authenticated_user(self):
        self.test_paste_create_as_guest()
        self.test_paste_create_as_user()
        url = reverse('paste-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_only_user_paste_list_for_authenticated_user(self):
        self.test_paste_create_as_guest()
        self.test_paste_create_as_user()
        url = reverse('paste-me')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        for data in response.data:
            self.assertEqual(data.get('user', None), self.user.id)
