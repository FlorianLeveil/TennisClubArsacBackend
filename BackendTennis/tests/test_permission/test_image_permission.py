from datetime import date
from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_api_key.models import APIKey
from BackendTennis.models import User, Image
from BackendTennis.permissions.image_permissions import ImagePermissions
from BackendTennis.views.ImageView import ImageListCreateView, ImageRetrieveUpdateDestroyView


class ImagePermissionsTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            birthdate=date(1990, 1, 1)
        )

        self.superuser = User.objects.create_superuser(
            email='superuser@example.com',
            password='superpassword',
            first_name='Super',
            last_name='User',
            birthdate=date(1990, 1, 1)
        )

        self.api_key, self.key = APIKey.objects.create_key(name="test-api-key")

        self.token = str(AccessToken.for_user(self.user))
        self.superuser_token = str(AccessToken.for_user(self.superuser))

        self.factory = APIRequestFactory()
        self.permission = ImagePermissions()

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
