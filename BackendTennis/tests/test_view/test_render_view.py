from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User, Render


class RenderViewTests(APITestCase):

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

        cls.render = Render.objects.create(
            navBarPosition='left',
            type='nav_bar'
        )

        cls.url = '/BackendTennis/render/'
        cls.detail_url = f'{cls.url}{cls.render.id}/'

    def test_get_render_list_no_authentication(self):
        """ Test if unauthenticated users cannot access the render list """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_get_render_list_with_api_key(self):
        """ Test if users with API key can access the render list """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

    def test_create_render_no_permission(self):
        data = {
            'navBarPosition': 'left',
            'type': 'nav_bar',
            'order': 2
        }
        """ Test creating a render without permission """
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_create_render_with_permission(self):
        """ Test creating a render with correct permissions """
        data = {
            'navBarPosition': 'left',
            'type': 'nav_bar',
            'order': 2
        }
        permission = Permission.objects.get(codename='add_render')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_get_render_detail_with_api_key(self):
        """ Test retrieving a render detail """
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.assertEqual(response.data['navBarPosition'], self.render.navBarPosition, str(response.data))

    def test_update_render_no_permission(self):
        """ Test updating a render without permission """
        data = {
            'navBarPosition': 'left',
            'type': 'nav_bar',
            'order': 2
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_update_render_with_permission(self):
        """ Test updating a render with correct permissions """
        data = {
            'navBarPosition': 'right',
            'type': 'home_page',
            'order': 2
        }
        permission = Permission.objects.get(codename='change_render')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.render.refresh_from_db()
        self.assertEqual(self.render.navBarPosition, 'right', str(response.data))

    def test_delete_render_no_permission(self):
        """ Test deleting a render without permission """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_delete_render_with_permission(self):
        """ Test deleting a render with correct permissions """
        permission = Permission.objects.get(codename='delete_render')
        self.user.user_permissions.add(permission)
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(Render.objects.count(), 0, str(response.data))

    def test_superuser_can_create_render(self):
        """ Test if a superuser can create a render """
        data = {
            'navBarPosition': 'left',
            'type': 'nav_bar',
            'order': 2
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_superuser_can_update_render(self):
        """ Test if a superuser can update a render """
        data = {
            'navBarPosition': 'left',
            'type': 'nav_bar',
            'order': 2
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.render.refresh_from_db()
        self.assertEqual(self.render.navBarPosition, 'left', str(response.data))

    def test_superuser_can_delete_render(self):
        """ Test if a superuser can delete a render """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key,
                                      HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(Render.objects.count(), 0, str(response.data))
