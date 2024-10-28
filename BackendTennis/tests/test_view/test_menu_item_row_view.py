from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User, MenuItemRow, Route


class MenuItemRowViewTests(APITestCase):

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

        cls.route = Route.objects.create(
            name='New Test Route',
            protocol='https',
            domainUrl='test.com'
        )

        cls.menu_item_row = MenuItemRow.objects.create(
            title='New Test MenuItemRow',
            route=cls.route,
            color='green',
            order=1
        )

        cls.url = '/BackendTennis/menu_item_row/'
        cls.detail_url = f'{cls.url}{cls.menu_item_row.id}/'

    def test_get_menu_item_row_list_no_authentication(self):
        """ Test if unauthenticated users cannot access the menu_item_row list """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_get_menu_item_row_list_with_api_key(self):
        """ Test if users with API key can access the menu_item_row list """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

    def test_create_menu_item_row_no_permission(self):
        data = {
            'title': 'New Test MenuItemRow',
        }
        """ Test creating a menu_item_row without permission """
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_create_menu_item_row_with_permission(self):
        """ Test creating a menu_item_row with correct permissions """
        data = {
            'title': 'New Test MenuItemRow',
        }
        permission = Permission.objects.get(codename='add_menuitemrow')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_get_menu_item_row_detail_with_api_key(self):
        """ Test retrieving a menu_item_row detail """
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.assertEqual(response.data['title'], self.menu_item_row.title, str(response.data))

    def test_update_menu_item_row_no_permission(self):
        """ Test updating a menu_item_row without permission """
        data = {
            'title': 'New Test MenuItemRow',
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_update_menu_item_row_with_permission(self):
        """ Test updating a menu_item_row with correct permissions """
        data = {
            'title': 'Updated Test MenuItemRow',
        }
        permission = Permission.objects.get(codename='change_menuitemrow')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.menu_item_row.refresh_from_db()
        self.assertEqual(self.menu_item_row.title, 'Updated Test MenuItemRow', str(response.data))

    def test_delete_menu_item_row_no_permission(self):
        """ Test deleting a menu_item_row without permission """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_delete_menu_item_row_with_permission(self):
        """ Test deleting a menu_item_row with correct permissions """
        permission = Permission.objects.get(codename='delete_menuitemrow')
        self.user.user_permissions.add(permission)
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(MenuItemRow.objects.count(), 0, str(response.data))

    def test_superuser_can_create_menu_item_row(self):
        """ Test if a superuser can create a menu_item_row """
        data = {
            'title': 'New Test MenuItemRow',
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_superuser_can_update_menu_item_row(self):
        """ Test if a superuser can update a menu_item_row """
        data = {
            'title': 'Updated Test MenuItemRow',
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.menu_item_row.refresh_from_db()
        self.assertEqual(self.menu_item_row.title, 'Updated Test MenuItemRow', str(response.data))

    def test_superuser_can_delete_menu_item_row(self):
        """ Test if a superuser can delete a menu_item_row """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key,
                                      HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(MenuItemRow.objects.count(), 0, str(response.data))
