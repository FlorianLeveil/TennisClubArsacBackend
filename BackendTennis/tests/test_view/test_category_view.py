from datetime import date
from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken
from BackendTennis.models import User, Category
from rest_framework import status


class CategoryViewTests(APITestCase):

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

        # JWT tokens for users
        self.token = str(AccessToken.for_user(self.user))
        self.superuser_token = str(AccessToken.for_user(self.superuser))

        self.category = Category.objects.create(name="Existing Category", icon="test_icon.jpg")

        self.url = '/BackendTennis/category/'
        self.detail_url = f'{self.url}{self.category.id}/'

    def test_get_category_list_no_authentication(self):
        """ Test fetching category list without authentication (should be forbidden) """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_category_list_with_api_key(self):
        """ Test fetching category list with API key (should succeed) """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_no_permission(self):
        """ Test creating a category without 'add_category' permission (should be forbidden) """
        data = {
            'name': 'New Category',
            'icon': 'new_icon.jpg'
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_with_permission(self):
        """ Test creating a category with 'add_category' permission (should succeed) """
        data = {
            'name': 'New Category',
            'icon': 'new_icon.jpg'
        }
        permission = Permission.objects.get(codename='add_category')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superuser_can_create_category(self):
        """ Test if a superuser can create a category (should succeed) """
        data = {
            'name': 'Super Category',
            'icon': 'super_icon.jpg'
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_category_no_permission(self):
        """ Test updating a category without 'change_category' permission (should be forbidden) """
        data = {'name': 'Updated Category'}
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_with_permission(self):
        """ Test updating a category with 'change_category' permission (should succeed) """
        data = {'name': 'Updated Category'}
        permission = Permission.objects.get(codename='change_category')
        self.user.user_permissions.add(permission)
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_superuser_can_update_category(self):
        """ Test if a superuser can update a category (should succeed) """
        data = {'name': 'Super Updated Category'}
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Super Updated Category')

    def test_delete_category_no_permission(self):
        """ Test deleting a category without 'delete_category' permission (should be forbidden) """
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_with_permission(self):
        """ Test deleting a category with 'delete_category' permission (should succeed) """
        permission = Permission.objects.get(codename='delete_category')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_superuser_can_delete_category(self):
        """ Test if a superuser can delete a category (should succeed) """
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
