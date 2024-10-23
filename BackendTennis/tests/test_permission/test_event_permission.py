from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.constant import Constant
from BackendTennis.models import User, Event, Image, Category


class EventPermissionsTests(APITestCase):

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

        cls.image = Image.objects.create(title="Test Image", type=Constant.IMAGE_TYPE.EVENT)
        cls.category = Category.objects.create(name="Test Category")

        cls.token = str(AccessToken.for_user(cls.user))
        cls.superuser_token = str(AccessToken.for_user(cls.superuser))

        cls.api_key, cls.key = APIKey.objects.create_key(name="test-api-key")

        cls.event = Event.objects.create(
            title='Existing Event',
            description='This is a test event',
            dateType='single',
            start='2024-09-01T10:00:00Z',
            end='2024-09-01T12:00:00Z',
            image=cls.image,
            category=cls.category
        )

        cls.url = '/BackendTennis/event/'
        cls.detail_url = f'{cls.url}{cls.event.id}/'

    def test_get_event_list_no_authentication(self):
        """ Test fetching event list without authentication (should be forbidden) """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_event_list_with_api_key(self):
        """ Test fetching event list with API key (should succeed) """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_event_no_permission(self):
        """ Test creating an event without 'add_event' permission (should be forbidden) """
        data = {
            'title': 'New Event',
            'description': 'This is a new event',
            'dateType': 'single',
            'start': '2024-09-02T10:00:00Z',
            'end': '2024-09-02T12:00:00Z',
            'image': self.image.id,
            'category': self.category.id
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_event_with_permission(self):
        """ Test creating an event with 'add_event' permission (should succeed) """
        data = {
            'title': 'New Event',
            'description': 'This is a new event',
            'dateType': 'single',
            'start': '2024-09-02T10:00:00Z',
            'end': '2024-09-02T12:00:00Z',
            'image': self.image.id,
            'category': self.category.id
        }
        permission = Permission.objects.get(codename='add_event')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superuser_can_create_event(self):
        """ Test if a superuser can create an event (should succeed) """
        data = {
            'title': 'Super Event',
            'description': 'This is a super event',
            'dateType': 'single',
            'start': '2024-09-02T10:00:00Z',
            'end': '2024-09-02T12:00:00Z',
            'image': self.image.id,
            'category': self.category.id
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_event_no_permission(self):
        """ Test updating an event without 'change_event' permission (should be forbidden) """
        data = {'title': 'Updated Event'}
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_event_with_permission(self):
        """ Test updating an event with 'change_event' permission (should succeed) """
        data = {'title': 'Updated Event'}
        permission = Permission.objects.get(codename='change_event')
        self.user.user_permissions.add(permission)
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_can_update_event(self):
        """ Test if a superuser can update an event (should succeed) """
        data = {'title': 'Super Updated Event'}
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_event_no_permission(self):
        """ Test deleting an event without 'delete_event' permission (should be forbidden) """
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_event_with_permission(self):
        """ Test deleting an event with 'delete_event' permission (should succeed) """
        permission = Permission.objects.get(codename='delete_event')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_superuser_can_delete_event(self):
        """ Test if a superuser can delete an event (should succeed) """
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
