from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User, Route


class RouteViewTests(APITestCase):

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

        cls.url = '/BackendTennis/route/'
        cls.detail_url = f'{cls.url}{cls.route.id}/'

    def test_get_route_list_no_authentication(self):
        """ Test if unauthenticated users cannot access the route list """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_get_route_list_with_api_key(self):
        """ Test if users with API key can access the route list """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

    def test_create_route_no_permission(self):
        data = {
            'name': 'New Test Route',
            'protocol': 'https',
            'domainUrl': 'new_test.com'
        }
        """ Test creating a route without permission """
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_create_route_with_permission(self):
        """ Test creating a route with correct permissions """
        data = {
            'name': 'New Test Route',
            'protocol': 'https',
            'domainUrl': 'new_test.com'
        }
        permission = Permission.objects.get(codename='add_route')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_get_route_detail_with_api_key(self):
        """ Test retrieving a route detail """
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.assertEqual(response.data['name'], self.route.name, str(response.data))

    def test_update_route_no_permission(self):
        """ Test updating a route without permission """
        data = {
            'name': 'Updated Test Route'
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_update_route_with_permission(self):
        """ Test updating a route with correct permissions """
        data = {
            'name': 'Updated Test Route'
        }
        permission = Permission.objects.get(codename='change_route')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.route.refresh_from_db()
        self.assertEqual(self.route.name, 'Updated Test Route', str(response.data))

    def test_delete_route_no_permission(self):
        """ Test deleting a route without permission """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_delete_route_with_permission(self):
        """ Test deleting a route with correct permissions """
        permission = Permission.objects.get(codename='delete_route')
        self.user.user_permissions.add(permission)
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(Route.objects.count(), 0, str(response.data))

    def test_superuser_can_create_route(self):
        """ Test if a superuser can create a route """
        data = {
            'name': 'New Test Route',
            'protocol': 'https',
            'domainUrl': 'new_test.com'
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_superuser_can_update_route(self):
        """ Test if a superuser can update a route """
        data = {
            'name': 'Updated Test Route'
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.route.refresh_from_db()
        self.assertEqual(self.route.name, 'Updated Test Route', str(response.data))

    def test_superuser_can_delete_route(self):
        """ Test if a superuser can delete a route """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key,
                                      HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(Route.objects.count(), 0, str(response.data))
