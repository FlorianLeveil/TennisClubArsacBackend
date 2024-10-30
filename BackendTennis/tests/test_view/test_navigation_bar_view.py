from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.constant import Constant
from BackendTennis.models import NavigationBar, User, Image


class NavigationBarViewTests(APITestCase):

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

        cls.image = Image.objects.create(title='NavigationBar Image', type=Constant.IMAGE_TYPE.NAVIGATION_BAR)
        cls.image_2 = Image.objects.create(title='NavigationBar Image 2', type=Constant.IMAGE_TYPE.NAVIGATION_BAR)
        cls.navigation_bar_data = {
            'logo': cls.image_2.id,
        }
        cls.navigation_bar = NavigationBar.objects.create(
            logo=cls.image
        )

        cls.url = '/BackendTennis/navigation_bar/'
        cls.detail_url = f'{cls.url}{cls.navigation_bar.id}/'

    def test_get_navigation_bar_list_no_authentication(self):
        """ Test if unauthenticated users cannot access the navigation_bar list """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_get_navigation_bar_list_with_api_key(self):
        """ Test if users with API key can access the navigation_bar list """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

    def test_create_navigation_bar_no_permission(self):
        """ Test creating a navigation_bar without permission """
        response = self.client.post(self.url, data=self.navigation_bar_data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_create_navigation_bar_with_permission(self):
        """ Test creating a navigation_bar with correct permissions """
        permission = Permission.objects.get(codename='add_navigationbar')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=self.navigation_bar_data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_get_navigation_bar_detail_with_api_key(self):
        """ Test retrieving a navigation_bar detail """
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.assertEqual(response.data['logo'], self.navigation_bar.logo.id, str(response.data))

    def test_update_navigation_bar_no_permission(self):
        """ Test updating a navigation_bar without permission """
        response = self.client.patch(self.detail_url, data=self.navigation_bar_data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_update_navigation_bar_with_permission(self):
        """ Test updating a navigation_bar with correct permissions """
        permission = Permission.objects.get(codename='change_navigationbar')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=self.navigation_bar_data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.navigation_bar.refresh_from_db()
        self.assertEqual(self.navigation_bar.logo.id, self.image_2.id, str(response.data))

    def test_delete_navigation_bar_no_permission(self):
        """ Test deleting a navigation_bar without permission """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_delete_navigation_bar_with_permission(self):
        """ Test deleting a navigation_bar with correct permissions """
        permission = Permission.objects.get(codename='delete_navigationbar')
        self.user.user_permissions.add(permission)
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(NavigationBar.objects.count(), 0, str(response.data))

    def test_superuser_can_create_navigation_bar(self):
        """ Test if a superuser can create a navigation_bar """
        response = self.client.post(self.url, data=self.navigation_bar_data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))

    def test_superuser_can_update_navigation_bar(self):
        """ Test if a superuser can update a navigation_bar """
        response = self.client.patch(self.detail_url, data=self.navigation_bar_data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.navigation_bar.refresh_from_db()
        self.assertEqual(self.navigation_bar.logo.id, self.image_2.id, str(response.data))

    def test_superuser_can_delete_navigation_bar(self):
        """ Test if a superuser can delete a navigation_bar """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key,
                                      HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(NavigationBar.objects.count(), 0, str(response.data))
