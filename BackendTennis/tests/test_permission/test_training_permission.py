from datetime import date, datetime

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User, Training


class TrainingPermissionsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            birthdate=date(1990, 1, 1)

        )

        cls.superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User',
            birthdate=date(1990, 1, 1)
        )

        cls.token = str(AccessToken.for_user(cls.user))

        cls.admin_token = str(AccessToken.for_user(cls.superuser))

        cls.api_key, cls.key = APIKey.objects.create_key(name="test-api-key")

        cls.training = Training.objects.create(
            name='Test Training',
            unregisteredParticipants=[],
            cancel=False,
            start=datetime(2024, 10, 12),
            end=datetime(2024, 10, 13)
        )
        cls.training.participants.set([cls.user.id])

        cls.url = '/BackendTennis/training/'
        cls.detail_url = f'{cls.url}{cls.training.id}/'

    def test_get_training_list(self):
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_training_list_with_invalid_api_key(self):
        response = self.client.get(self.url, HTTP_API_KEY="invalid_key")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_training_without_permission(self):
        data = {
            'name': 'Test Training',
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
            'start': datetime(2024, 10, 12),
            'end': datetime(2024, 10, 13),
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_training_with_permission(self):
        permission = Permission.objects.get(codename='add_training')
        self.user.user_permissions.add(permission)
        data = {
            'name': 'Test Training',
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
            'start': datetime(2024, 10, 12),
            'end': datetime(2024, 10, 13),
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_training_without_permission(self):
        data = {
            'name': 'Updated Training',
            'start': datetime(2024, 10, 15),
            'end': datetime(2024, 10, 16),
        }
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_training_with_permission(self):
        permission = Permission.objects.get(codename='change_training')
        self.user.user_permissions.add(permission)
        data = {
            'name': 'Updated Training',
            'start': datetime(2024, 10, 15),
            'end': datetime(2024, 10, 16),
        }
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_training_without_permission(self):
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_training_with_permission(self):
        permission = Permission.objects.get(codename='delete_training')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_superuser_can_post_training(self):
        data = {
            'name': 'Test Training',
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
            'start': datetime(2024, 10, 12),
            'end': datetime(2024, 10, 13),
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
