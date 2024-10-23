from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User, Booking


class BookingViewTests(APITestCase):

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

        cls.token = str(AccessToken.for_user(cls.user))
        cls.superuser_token = str(AccessToken.for_user(cls.superuser))
        cls.api_key, cls.key = APIKey.objects.create_key(name="test-api-key")

        cls.booking = Booking.objects.create(
            clientFirstName='John',
            clientLastName='Doe',
            clientEmail='john.doe@example.com',
            clientPhoneNumber='123456789',
            payed=True,
            insurance=False,
            color='blue',
            label='Booked',
            start=date(2024, 1, 1),
            end=date(2024, 1, 2)
        )

        cls.url = '/BackendTennis/booking/'
        cls.detail_url = f'{cls.url}{cls.booking.id}/'

    def test_get_booking_list_no_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_booking_list_with_api_key(self):
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_create_booking_permission(self):
        data = {
            'clientFirstName': 'Alice',
            'clientLastName': 'Smith',
            'clientEmail': 'alice.smith@example.com',
            'clientPhoneNumber': '987654321',
            'payed': False,
            'insurance': True,
            'color': 'green',
            'label': 'Reserved',
            'start': '2024-02-01',
            'end': '2024-02-02'
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_booking_with_permission(self):
        data = {
            'clientFirstName': 'Alice',
            'clientLastName': 'Smith',
            'clientEmail': 'alice.smith@example.com',
            'clientPhoneNumber': '987654321',
            'payed': False,
            'insurance': True,
            'color': 'green',
            'label': 'Reserved',
            'start': '2024-02-01',
            'end': '2024-02-02'
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_booking_no_permission(self):
        data = {'clientFirstName': 'Updated John'}
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_booking_with_permission(self):
        data = {'clientFirstName': 'Updated John'}
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.clientFirstName, 'Updated John')

    def test_delete_booking_no_permission(self):
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_booking_with_permission(self):
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
