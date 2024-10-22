from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import Pricing, User, Image


class PricingPermissionsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            birthdate=date(1990, 1, 1)

        )

        self.superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User',
            birthdate=date(1990, 1, 1)
        )

        self.token = str(AccessToken.for_user(self.user))

        self.admin_token = str(AccessToken.for_user(self.superuser))

        self.api_key, self.key = APIKey.objects.create_key(name="test-api-key")

        self.image = Image.objects.create(type='sponsor', imageUrl='test_image_url.jpg')
        self.pricing = Pricing.objects.create(
            title="Test Pricing",
            license="Test description",
            site_access="Test description",
            extra_data=[{"label": "Test extra data", "value": "Test value", "type": "string"}],
            information="Test information",
            price=100.0,
            type="adult",
            image=self.image
        )

        self.url = '/BackendTennis/pricing/'
        self.detail_url = f'{self.url}{self.pricing.id}/'

    def test_get_pricing_list(self):
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_pricing_list_with_invalid_api_key(self):
        response = self.client.get(self.url, HTTP_API_KEY="invalid_key")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_pricing_without_permission(self):
        data = {
            'title': 'New Pricing',
            'description': 'New Description',
            'price': 200.0,
            'type': 'adult',
            'image': self.image.id
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_pricing_with_permission(self):
        permission = Permission.objects.get(codename='add_pricing')
        self.user.user_permissions.add(permission)
        data = {
            'title': 'New Pricing',
            'description': 'New Description',
            'price': 200.0,
            'type': 'adult',
            'image': self.image.id
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_pricing_without_permission(self):
        data = {
            'title': 'Updated Pricing',
            'price': 150.0
        }
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_pricing_with_permission(self):
        permission = Permission.objects.get(codename='change_pricing')
        self.user.user_permissions.add(permission)
        data = {
            'title': 'Updated Pricing',
            'price': 150.0
        }
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_pricing_without_permission(self):
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_pricing_with_permission(self):
        permission = Permission.objects.get(codename='delete_pricing')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_superuser_can_post_pricing(self):
        data = {
            'title': 'New Pricing',
            'description': 'New Description',
            'price': 200.0,
            'type': 'adult',
            'image': self.image.id
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
