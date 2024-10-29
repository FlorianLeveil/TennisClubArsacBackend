from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User, MenuItem


class MenuItemViewTests(APITestCase):

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

        cls.menu_item = MenuItem.objects.create(
            title='New Test MenuItem',
        )

        cls.url = '/BackendTennis/menu_item/'
        cls.detail_url = f'{cls.url}{cls.menu_item.id}/'

    def test_get_menu_item_list_no_authentication(self):
        """ Test if unauthenticated users cannot access the menu_item list """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_get_menu_item_list_with_api_key(self):
        """ Test if users with API key can access the menu_item list """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

    def test_create_menu_item_no_permission(self):
        data = {
            'title': 'New Test MenuItem',
        }
        """ Test creating a menu_item without permission """
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_create_menu_item_with_permission(self):
        """ Test creating a menu_item with correct permissions """
        data = {
            'title': 'New Test MenuItem',
            'order': 1
        }
        permission = Permission.objects.get(codename='add_menuitem')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_get_menu_item_detail_with_api_key(self):
        """ Test retrieving a menu_item detail """
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.assertEqual(response.data['title'], self.menu_item.title, str(response.data))

    def test_update_menu_item_no_permission(self):
        """ Test updating a menu_item without permission """
        data = {
            'title': 'New Test MenuItem',
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_update_menu_item_with_permission(self):
        """ Test updating a menu_item with correct permissions """
        data = {
            'title': 'Updated Test MenuItem',
            'order': 1
        }
        permission = Permission.objects.get(codename='change_menuitem')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.title, 'Updated Test MenuItem', str(response.data))

    def test_delete_menu_item_no_permission(self):
        """ Test deleting a menu_item without permission """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_delete_menu_item_with_permission(self):
        """ Test deleting a menu_item with correct permissions """
        permission = Permission.objects.get(codename='delete_menuitem')
        self.user.user_permissions.add(permission)
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(MenuItem.objects.count(), 0, str(response.data))

    def test_superuser_can_create_menu_item(self):
        """ Test if a superuser can create a menu_item """
        data = {
            'title': 'New Test MenuItem',
            'order': 1
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_superuser_can_update_menu_item(self):
        """ Test if a superuser can update a menu_item """
        data = {
            'title': 'Updated Test MenuItem',
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.title, 'Updated Test MenuItem', str(response.data))

    def test_superuser_can_delete_menu_item(self):
        """ Test if a superuser can delete a menu_item """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key,
                                      HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(MenuItem.objects.count(), 0, str(response.data))
