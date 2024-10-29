from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User, Render, Route, PageRender


class PageRenderPermissionsTests(APITestCase):

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

        cls.api_key, cls.key = APIKey.objects.create_key(name='test-api-key')

        cls.render = Render.objects.create(
            navBarPosition='left',
            type='nav_bar'
        )

        cls.route = Route.objects.create(
            name='Test Route',
            protocol='https',
            domainUrl='test.com'
        )

        cls.page_render = PageRender.objects.create(
            route=cls.route,
            render=cls.render
        )

        cls.url = '/BackendTennis/page_render/'
        cls.detail_url = f'{cls.url}{cls.page_render.id}/'

    def test_get_page_render_list_no_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_get_page_render_list_with_api_key(self):
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

    def test_create_page_render_no_permission(self):
        data = {
            'route': self.route.id,
            'render': self.render.id
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_create_page_render_with_permission(self):
        data = {
            'route': self.route.id,
            'render': self.render.id
        }
        permission = Permission.objects.get(codename='add_pagerender')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_superuser_can_create_page_render(self):
        data = {
            'route': self.route.id,
            'render': self.render.id
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_update_page_render_no_permission(self):
        data = {
            'route': self.route.id,
            'render': self.render.id
        }
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_update_page_render_with_permission(self):
        data = {
            'route': self.route.id,
            'render': self.render.id
        }
        permission = Permission.objects.get(codename='change_pagerender')
        self.user.user_permissions.add(permission)
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

    def test_superuser_can_update_page_render(self):
        data = {
            'route': self.route.id,
            'render': self.render.id
        }
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

    def test_delete_page_render_no_permission(self):
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_delete_page_render_with_permission(self):
        permission = Permission.objects.get(codename='delete_pagerender')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))

    def test_superuser_can_delete_page_render(self):
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
