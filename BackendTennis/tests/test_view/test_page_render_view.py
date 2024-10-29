from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import PageRender, User, Render, Route


class PageRenderViewTests(APITestCase):

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

        cls.route = Route.objects.create(
            name='Test Route',
            protocol='https',
            domainUrl='test.com'
        )

        cls.route_2 = Route.objects.create(
            name='Test Route 2',
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
        """ Test if unauthenticated users cannot access the page_render list """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_get_page_render_list_with_api_key(self):
        """ Test if users with API key can access the page_render list """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

    def test_create_page_render_no_permission(self):
        data = {
            'route': self.route.id,
            'render': self.render.id
        }
        """ Test creating a page_render without permission """
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_create_page_render_with_permission(self):
        """ Test creating a page_render with correct permissions """
        data = {
            'route': self.route.id,
            'render': self.render.id
        }
        permission = Permission.objects.get(codename='add_pagerender')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_get_page_render_detail_with_api_key(self):
        """ Test retrieving a page_render detail """
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.assertEqual(response.data['route'], self.page_render.route.id, str(response.data))

    def test_update_page_render_no_permission(self):
        """ Test updating a page_render without permission """
        data = {
            'route': self.route.id,
            'render': self.render.id
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_update_page_render_with_permission(self):
        """ Test updating a page_render with correct permissions """
        data = {
            'route': self.route_2.id,
            'render': self.render.id
        }
        permission = Permission.objects.get(codename='change_pagerender')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.page_render.refresh_from_db()
        self.assertEqual(self.page_render.route.id, self.route_2.id, str(response.data))

    def test_delete_page_render_no_permission(self):
        """ Test deleting a page_render without permission """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_delete_page_render_with_permission(self):
        """ Test deleting a page_render with correct permissions """
        permission = Permission.objects.get(codename='delete_pagerender')
        self.user.user_permissions.add(permission)
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(PageRender.objects.count(), 0, str(response.data))

    def test_superuser_can_create_render(self):
        """ Test if a superuser can create a page_render """
        data = {
            'route': self.route.id,
            'render': self.render.id
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_superuser_can_update_render(self):
        """ Test if a superuser can update a page_render """
        data = {
            'route': self.route.id,
            'render': self.render.id
        }
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.page_render.refresh_from_db()
        self.assertEqual(self.page_render.route.id, self.route.id, str(response.data))

    def test_superuser_can_delete_render(self):
        """ Test if a superuser can delete a page_render """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key,
                                      HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(PageRender.objects.count(), 0, str(response.data))
