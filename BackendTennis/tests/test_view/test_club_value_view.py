from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User, ClubValue


class ClubValueViewTests(APITestCase):

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

        # JWT tokens for users
        cls.token = str(AccessToken.for_user(cls.user))
        cls.superuser_token = str(AccessToken.for_user(cls.superuser))

        cls.club_value = ClubValue.objects.create(
            title='ClubValue Title',
            description='ClubValue description',
            order=0
        )

        cls.url = '/BackendTennis/club_value/'
        cls.detail_url = f'{cls.url}{cls.club_value.id}/'

    def test_get_club_value_list_no_authentication(self):
        """ Test fetching club_value list without authentication (should be forbidden) """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_club_value_list_with_api_key(self):
        """ Test fetching club_value list with API key (should succeed) """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_club_value_no_permission(self):
        """ Test creating a club_value without 'add_club_value' permission (should be forbidden) """
        data = {
            'title': 'Tennis ClubValue',
            'description': 'Tennis ClubValue description',
            'order': 1
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_club_value_with_permission(self):
        """ Test creating a club_value with 'add_club_value' permission (should succeed) """
        data = {
            'title': 'Tennis ClubValue',
            'description': 'Tennis ClubValue description',
            'order': 1
        }
        permission = Permission.objects.get(codename='add_clubvalue')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superuser_can_create_club_value(self):
        """ Test if a superuser can create a club_value (should succeed) """
        data = {
            'title': 'Tennis ClubValue',
            'description': 'Tennis ClubValue description',
            'order': 1
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_club_value_no_permission(self):
        """ Test updating a club_value without 'change_club_value' permission (should be forbidden) """
        data = {'title': 'Updated ClubValue'}
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_club_value_with_permission(self):
        """ Test updating a club_value with 'change_club_value' permission (should succeed) """
        data = {'title': 'Updated ClubValue'}
        permission = Permission.objects.get(codename='change_clubvalue')
        self.user.user_permissions.add(permission)
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.club_value.refresh_from_db()
        self.assertEqual(self.club_value.title, 'Updated ClubValue')

    def test_superuser_can_update_club_value(self):
        """ Test if a superuser can update a club_value (should succeed) """
        data = {'title': 'Super Updated ClubValue'}
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.club_value.refresh_from_db()
        self.assertEqual(self.club_value.title, 'Super Updated ClubValue')

    def test_delete_club_value_no_permission(self):
        """ Test deleting a club_value without 'delete_club_value' permission (should be forbidden) """
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_club_value_with_permission(self):
        """ Test deleting a club_value with 'delete_club_value' permission (should succeed) """
        permission = Permission.objects.get(codename='delete_clubvalue')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_superuser_can_delete_club_value(self):
        """ Test if a superuser can delete a club_value (should succeed) """
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
