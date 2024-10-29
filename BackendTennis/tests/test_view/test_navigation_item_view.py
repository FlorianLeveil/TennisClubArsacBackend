from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User, NavigationItem


class NavigationItemViewTests(APITestCase):

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

        cls.navigation_item = NavigationItem.objects.create(
            title='New Test NavigationItem',
        )

        cls.url = '/BackendTennis/navigation_item/'
        cls.detail_url = f'{cls.url}{cls.navigation_item.id}/'

    def test_get_navigation_item_list_no_authentication(self):
        """ Test if unauthenticated users cannot access the navigation_item list """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_get_navigation_item_list_with_api_key(self):
        """ Test if users with API key can access the navigation_item list """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

    def test_create_navigation_item_no_permission(self):
        data = {
            'title': 'New Test NavigationItem',
        }
        """ Test creating a navigation_item without permission """
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_create_navigation_item_with_permission(self):
        """ Test creating a navigation_item with correct permissions """
        data = {
            'title': 'New Test NavigationItem',
        }
        permission = Permission.objects.get(codename='add_navigationitem')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_get_navigation_item_detail_with_api_key(self):
        """ Test retrieving a navigation_item detail """
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.assertEqual(response.data['title'], self.navigation_item.title, str(response.data))

    def test_update_navigation_item_no_permission(self):
        """ Test updating a navigation_item without permission """
        data = {
            'title': 'New Test NavigationItem',
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_update_navigation_item_with_permission(self):
        """ Test updating a navigation_item with correct permissions """
        data = {
            'title': 'Updated Test NavigationItem',
        }
        permission = Permission.objects.get(codename='change_navigationitem')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.navigation_item.refresh_from_db()
        self.assertEqual(self.navigation_item.title, 'Updated Test NavigationItem', str(response.data))

    def test_delete_navigation_item_no_permission(self):
        """ Test deleting a navigation_item without permission """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_delete_navigation_item_with_permission(self):
        """ Test deleting a navigation_item with correct permissions """
        permission = Permission.objects.get(codename='delete_navigationitem')
        self.user.user_permissions.add(permission)
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(NavigationItem.objects.count(), 0, str(response.data))

    def test_superuser_can_create_navigation_item(self):
        """ Test if a superuser can create a navigation_item """
        data = {
            'title': 'New Test NavigationItem',
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_superuser_can_update_navigation_item(self):
        """ Test if a superuser can update a navigation_item """
        data = {
            'title': 'Updated Test NavigationItem',
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.navigation_item.refresh_from_db()
        self.assertEqual(self.navigation_item.title, 'Updated Test NavigationItem', str(response.data))

    def test_superuser_can_delete_navigation_item(self):
        """ Test if a superuser can delete a navigation_item """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key,
                                      HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(NavigationItem.objects.count(), 0, str(response.data))
