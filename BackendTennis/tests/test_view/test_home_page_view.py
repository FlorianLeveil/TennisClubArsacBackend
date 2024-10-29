from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User, HomePage


class HomePageViewTests(APITestCase):

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

        cls.api_key, cls.key = APIKey.objects.create_key(name='test-api-key')
        cls.token = str(AccessToken.for_user(cls.user))
        cls.superuser_token = str(AccessToken.for_user(cls.superuser))

        cls.home_page = HomePage.objects.create(
            title='New Test HomePage',
        )

        cls.url = '/BackendTennis/home_page/'
        cls.detail_url = f'{cls.url}{cls.home_page.id}/'

    def test_get_home_page_list_no_authentication(self):
        """ Test if unauthenticated users cannot access the home_page list """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_get_home_page_list_with_api_key(self):
        """ Test if users with API key can access the home_page list """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

    def test_create_home_page_no_permission(self):
        data = {
            'title': 'New Test HomePage',
        }
        """ Test creating a home_page without permission """
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_create_home_page_with_permission(self):
        """ Test creating a home_page with correct permissions """
        data = {
            'title': 'New Test HomePage',
            'order': 1
        }
        permission = Permission.objects.get(codename='add_homepage')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_get_home_page_detail_with_api_key(self):
        """ Test retrieving a home_page detail """
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.assertEqual(response.data['title'], self.home_page.title, str(response.data))

    def test_update_home_page_no_permission(self):
        """ Test updating a home_page without permission """
        data = {
            'title': 'New Test HomePage',
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_update_home_page_with_permission(self):
        """ Test updating a home_page with correct permissions """
        data = {
            'title': 'Updated Test HomePage',
            'order': 1
        }
        permission = Permission.objects.get(codename='change_homepage')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.home_page.refresh_from_db()
        self.assertEqual(self.home_page.title, 'Updated Test HomePage', str(response.data))

    def test_delete_home_page_no_permission(self):
        """ Test deleting a home_page without permission """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_delete_home_page_with_permission(self):
        """ Test deleting a home_page with correct permissions """
        permission = Permission.objects.get(codename='delete_homepage')
        self.user.user_permissions.add(permission)
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(HomePage.objects.count(), 0, str(response.data))

    def test_superuser_can_create_home_page(self):
        """ Test if a superuser can create a home_page """
        data = {
            'title': 'New Test HomePage',
            'order': 1
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_superuser_can_update_home_page(self):
        """ Test if a superuser can update a home_page """
        data = {
            'title': 'Updated Test HomePage',
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.home_page.refresh_from_db()
        self.assertEqual(self.home_page.title, 'Updated Test HomePage', str(response.data))

    def test_superuser_can_delete_home_page(self):
        """ Test if a superuser can delete a home_page """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key,
                                      HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(HomePage.objects.count(), 0, str(response.data))
