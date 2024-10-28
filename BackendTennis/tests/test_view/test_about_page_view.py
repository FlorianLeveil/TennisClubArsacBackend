from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User, AboutPage


class AboutPageViewTests(APITestCase):

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

        cls.about_page = AboutPage.objects.create()

        cls.url = '/BackendTennis/about_page/'
        cls.detail_url = f'{cls.url}{cls.about_page.id}/'

    def test_get_about_page_list_no_authentication(self):
        """ Test if unauthenticated users cannot access the about_page list """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_about_page_list_with_api_key(self):
        """ Test if users with API key can access the about_page list """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_about_page_no_permission(self):
        data = {}
        """ Test creating an about_page without permission """
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_about_page_with_permission(self):
        """ Test creating an about_page with correct permissions """
        data = {}
        permission = Permission.objects.get(codename='add_aboutpage')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_about_page_detail_with_api_key(self):
        """ Test retrieving an about_page detail """
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['clubTitle'], self.about_page.clubTitle)

    def test_update_about_page_no_permission(self):
        """ Test updating an about_page without permission """
        data = {'professorsTitle': 'Updated AboutPage'}
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_about_page_with_permission(self):
        """ Test updating an about_page with correct permissions """
        data = {'clubTitle': 'Updated AboutPage'}
        permission = Permission.objects.get(codename='change_aboutpage')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.about_page.refresh_from_db()
        self.assertEqual(self.about_page.clubTitle, 'Updated AboutPage')

    def test_delete_about_page_no_permission(self):
        """ Test deleting an about_page without permission """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_about_page_with_permission(self):
        """ Test deleting an about_page with correct permissions """
        permission = Permission.objects.get(codename='delete_aboutpage')
        self.user.user_permissions.add(permission)
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AboutPage.objects.count(), 0)

    def test_superuser_can_create_about_page(self):
        """ Test if a superuser can create an about_page """
        data = {}
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superuser_can_update_about_page(self):
        """ Test if a superuser can update an about_page """
        data = {'clubTitle': 'Superuser Updated AboutPage'}
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.about_page.refresh_from_db()
        self.assertEqual(self.about_page.clubTitle, 'Superuser Updated AboutPage')

    def test_superuser_can_delete_about_page(self):
        """ Test if a superuser can delete an about_page """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key,
                                      HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AboutPage.objects.count(), 0)
