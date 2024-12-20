from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User
from BackendTennis.permissions.image_permissions import ImagePermissions
from BackendTennis.views.ImageView import ImageListCreateView, ImageRetrieveUpdateDestroyView


class ImagePermissionsTests(APITestCase):

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

        cls.token = str(AccessToken.for_user(cls.user))
        cls.superuser_token = str(AccessToken.for_user(cls.superuser))

        cls.factory = APIRequestFactory()
        cls.permission = ImagePermissions()

        cls.multiple_images_url = '/BackendTennis/images/'

    def test_safe_method_permissions(self):
        request = self.factory.get('/images/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        view = ImageListCreateView()
        self.assertTrue(self.permission.has_permission(request, view))

    def test_post_method_no_authentication(self):
        request = self.factory.post('/images/')
        request.user = None  # No user
        view = ImageListCreateView()
        self.assertFalse(self.permission.has_permission(request, view))

    def test_post_method_authenticated_no_permission(self):
        request = self.factory.post('/images/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        view = ImageListCreateView()

        self.assertFalse(self.permission.has_permission(request, view))

    def test_post_method_authenticated_with_permission(self):
        request = self.factory.post('/images/')
        permission = Permission.objects.get(codename='add_image')
        self.user.user_permissions.add(permission)
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        view = ImageListCreateView()

        self.assertTrue(self.permission.has_permission(request, view))

    def test_superuser_can_post_image(self):
        request = self.factory.post('/images/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.superuser_token}'
        view = ImageListCreateView()

        self.assertTrue(self.permission.has_permission(request, view))

    def test_put_method_no_authentication(self):
        request = self.factory.put('/images/')
        request.user = None  # No user
        view = ImageRetrieveUpdateDestroyView()

        self.assertFalse(self.permission.has_permission(request, view))

    def test_put_method_authenticated_no_permission(self):
        request = self.factory.put('/images/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        view = ImageRetrieveUpdateDestroyView()

        self.assertFalse(self.permission.has_permission(request, view))

    def test_put_method_authenticated_with_permission(self):
        request = self.factory.put('/images/')
        permission = Permission.objects.get(codename='change_image')
        self.user.user_permissions.add(permission)
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        view = ImageRetrieveUpdateDestroyView()

        self.assertTrue(self.permission.has_permission(request, view))

    def test_superuser_can_put_image(self):
        request = self.factory.put('/images/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.superuser_token}'  # Superuser JWT Token
        view = ImageRetrieveUpdateDestroyView()

        self.assertTrue(self.permission.has_permission(request, view))

    def test_delete_method_no_authentication(self):
        request = self.factory.delete('/images/')
        request.user = None  # No user
        view = ImageRetrieveUpdateDestroyView()

        self.assertFalse(self.permission.has_permission(request, view))

    def test_delete_method_authenticated_no_permission(self):
        request = self.factory.delete('/images/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'  # JWT Token
        view = ImageRetrieveUpdateDestroyView()

        self.assertFalse(self.permission.has_permission(request, view))

    def test_delete_method_authenticated_with_permission(self):
        request = self.factory.delete('/images/')
        permission = Permission.objects.get(codename='delete_image')
        self.user.user_permissions.add(permission)
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        view = ImageRetrieveUpdateDestroyView()

        self.assertTrue(self.permission.has_permission(request, view))

    def test_superuser_can_delete_image(self):
        request = self.factory.delete('/images/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.superuser_token}'  # Superuser JWT Token
        view = ImageRetrieveUpdateDestroyView()

        self.assertTrue(self.permission.has_permission(request, view))

    def test_delete_navigation_item_no_permission(self):
        response = self.client.delete(
            self.multiple_images_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_delete_navigation_item_with_permission(self):
        permission = Permission.objects.get(codename='delete_image')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.multiple_images_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, str(response.data))

    def test_superuser_can_delete_navigation_item(self):
        response = self.client.delete(
            self.multiple_images_url,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, str(response.data))
