from datetime import datetime, timedelta, date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.constant import Constant
from BackendTennis.models import User, Event, Category, Image


class EventViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Setup user and tokens
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

        cls.category = Category.objects.create(name="Test Category")
        cls.image = Image.objects.create(type=Constant.IMAGE_TYPE.EVENT, imageUrl="test_image_url.jpg")

        cls.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            dateType="single-day",
            start=datetime.now() + timedelta(days=1),
            end=datetime.now() + timedelta(days=2),
            image=cls.image,
            category=cls.category
        )

        cls.url = '/BackendTennis/event/'
        cls.detail_url = f'{cls.url}{cls.event.id}/'

    def test_get_event_list_no_authentication(self):
        """ Test if unauthenticated users cannot access the event list """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_event_list_with_api_key(self):
        """ Test if users with API key can access the event list """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_event_list_with_mode_future(self):
        """ Test filtering events by mode 'FUTURE_EVENT' """
        response = self.client.get(f'{self.url}?mode=future_event', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['data'][0]['title'], "Test Event")

    def test_get_event_list_with_mode_history(self):
        """ Test filtering events by mode 'HISTORY' """
        Event.objects.create(
            title="Past Event",
            description="Past Description",
            dateType="single-day",
            start=datetime.now() - timedelta(days=10),
            end=datetime.now() - timedelta(days=5),
            image=self.image,
            category=self.category
        )
        response = self.client.get(f'{self.url}?mode=history', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['data'][0]['title'], "Past Event")

    def test_create_event_no_permission(self):
        """ Test creating an event without permission """
        data = {
            'title': 'New Event',
            'description': 'New Description',
            'dateType': 'single-day',
            'start': (datetime.now() + timedelta(days=5)).isoformat(),
            'end': (datetime.now() + timedelta(days=6)).isoformat(),
            'image': self.image.id,
            'category': self.category.id
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_event_with_permission(self):
        """ Test creating an event with correct permissions """
        data = {
            'title': 'New Event',
            'description': 'New Description',
            'dateType': 'single-day',
            'start': (datetime.now() + timedelta(days=5)).isoformat(),
            'end': (datetime.now() + timedelta(days=6)).isoformat(),
            'image': self.image.id,
            'category': self.category.id
        }
        permission = Permission.objects.get(codename='add_event')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_event_detail_with_api_key(self):
        """ Test retrieving an event detail """
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.event.title)

    def test_update_event_no_permission(self):
        """ Test updating an event without permission """
        data = {'title': 'Updated Event'}
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_event_with_permission(self):
        """ Test updating an event with correct permissions """
        data = {'title': 'Updated Event'}
        permission = Permission.objects.get(codename='change_event')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Updated Event')

    def test_delete_event_no_permission(self):
        """ Test deleting an event without permission """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_event_with_permission(self):
        """ Test deleting an event with correct permissions """
        permission = Permission.objects.get(codename='delete_event')
        self.user.user_permissions.add(permission)
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)

    def test_superuser_can_create_event(self):
        """ Test if a superuser can create an event """
        data = {
            'title': 'Superuser Event',
            'description': 'Superuser Description',
            'dateType': 'single-day',
            'start': (datetime.now() + timedelta(days=5)).isoformat(),
            'end': (datetime.now() + timedelta(days=6)).isoformat(),
            'image': self.image.id,
            'category': self.category.id
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superuser_can_update_event(self):
        """ Test if a superuser can update an event """
        data = {'title': 'Superuser Updated Event'}
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Superuser Updated Event')

    def test_superuser_can_delete_event(self):
        """ Test if a superuser can delete an event """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key,
                                      HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)
