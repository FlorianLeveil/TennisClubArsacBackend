from datetime import datetime, date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User, Training


class TrainingSerializerTestCase(APITestCase):

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
            email='superuser@example.com',
            password='superpassword',
            first_name='Super',
            last_name='User',
            birthdate=date(1990, 1, 1)
        )

        cls.api_key, cls.key = APIKey.objects.create_key(name="test-api-key")
        cls.token = str(AccessToken.for_user(cls.user))
        cls.superuser_token = str(AccessToken.for_user(cls.superuser))

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

    def test_get_training_list_no_authentication(self):
        """ Test if unauthenticated users cannot access the training list """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_training_list_with_api_key(self):
        """ Test if users with API key can access the training list """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_training_list_with_start_date_only_1_training(self):
        """ Test filtering trainings by start_date """
        _date = datetime(2024, 10, 11)
        response = self.client.get(f'{self.url}?start_date={_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['data'][0]['name'], "Test Training")

    def test_get_training_list_with_start_date_only_0_training(self):
        """ Test filtering trainings by start_date """
        _date = datetime(2024, 10, 14)
        response = self.client.get(f'{self.url}?start_date={_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_get_training_list_with_end_date_only_1_training(self):
        """ Test filtering trainings by end_date """
        _date = datetime(2024, 10, 14)
        response = self.client.get(f'{self.url}?end_date={_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['data'][0]['name'], "Test Training")

    def test_get_training_list_with_end_date_only_0_training(self):
        """ Test filtering trainings by end_date """
        _date = datetime(2024, 10, 10)
        response = self.client.get(f'{self.url}?end_date={_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_get_training_list_with_star_date_end_date_1_training(self):
        """ Test filtering trainings by start_date and end_date """
        start_date = datetime(2024, 10, 10)
        end_date = datetime(2024, 10, 15)
        response = self.client.get(f'{self.url}?start_date={start_date}&end_date={end_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['data'][0]['name'], "Test Training")

    def test_get_training_list_with_start_date_end_date_0_training(self):
        """ Test filtering trainings by start_date and end_date """
        start_date = datetime(2024, 10, 15)
        end_date = datetime(2024, 10, 16)
        response = self.client.get(f'{self.url}?start_date={start_date}&end_date={end_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_create_training_no_permission(self):
        data = {
            'name': 'Test Training',
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
            'start': datetime(2024, 10, 12),
            'end': datetime(2024, 10, 13),
        }
        """ Test creating a training without permission """
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_training_with_permission(self):
        """ Test creating a training with correct permissions """
        data = {
            'name': 'Test Training',
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
            'start': datetime(2024, 10, 12),
            'end': datetime(2024, 10, 13),
        }
        permission = Permission.objects.get(codename='add_training')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_training_detail_with_api_key(self):
        """ Test retrieving a training detail """
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.training.name)

    def test_update_training_no_permission(self):
        """ Test updating a training without permission """
        data = {'name': 'Updated Training'}
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_training_with_permission(self):
        """ Test updating a training with correct permissions """
        data = {'name': 'Updated Training'}
        permission = Permission.objects.get(codename='change_training')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.training.refresh_from_db()
        self.assertEqual(self.training.name, 'Updated Training')

    def test_delete_training_no_permission(self):
        """ Test deleting a training without permission """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_training_with_permission(self):
        """ Test deleting a training with correct permissions """
        permission = Permission.objects.get(codename='delete_training')
        self.user.user_permissions.add(permission)
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Training.objects.count(), 0)

    def test_superuser_can_create_training(self):
        """ Test if a superuser can create a training """
        data = {
            'name': 'Test Training',
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
            'start': datetime(2024, 10, 12),
            'end': datetime(2024, 10, 13),
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superuser_can_update_training(self):
        """ Test if a superuser can update a training """
        data = {'name': 'Superuser Updated Training'}
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.training.refresh_from_db()
        self.assertEqual(self.training.name, 'Superuser Updated Training')

    def test_superuser_can_delete_training(self):
        """ Test if a superuser can delete a training """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key,
                                      HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Training.objects.count(), 0)
