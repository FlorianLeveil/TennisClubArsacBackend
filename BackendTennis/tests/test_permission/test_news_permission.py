from datetime import date
from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken
from BackendTennis.models import User, News, Image, Category
from BackendTennis.serializers import NewsSerializer


class NewsPermissionsTests(APITestCase):

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

        self.image = Image.objects.create(type='news', imageUrl='test_image_url.jpg')
        self.category = Category.objects.create(name="Test Category")

        self.token = str(AccessToken.for_user(self.user))
        self.superuser_token = str(AccessToken.for_user(self.superuser))

        self.api_key, self.key = APIKey.objects.create_key(name="test-api-key")

        self.news = News.objects.create(
            title="Existing News",
            content="This is a test content",
            subtitle="Test subtitle",
            category=self.category
        )
        self.news.images.add(self.image)

        self.url = '/BackendTennis/news/'
        self.detail_url = f'{self.url}{self.news.id}/'

    def test_get_news_list_no_authentication(self):
        """Test if unauthenticated users can access news list (safe methods)"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_news_list_with_api_key(self):
        """Test if users with an API key can access news list (safe methods)"""
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_news_no_permission(self):
        """Test if a user without permissions can't create news"""
        data = {
            'title': 'New News',
            'content': 'This is a test content',
            'subtitle': 'New subtitle',
            'category': self.category.id,
            'images': [self.image.id]
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_news_with_permission(self):
        """Test if a user with permission can create news"""
        data = {
            'title': 'New News',
            'content': 'This is a test content',
            'subtitle': 'New subtitle',
            'category': self.category.id,
            'images': [self.image.id]
        }
        permission = Permission.objects.get(codename='add_news')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superuser_can_create_news(self):
        """Test if a superuser can create news"""
        data = {
            'title': 'Super News',
            'content': 'Super content',
            'subtitle': 'Super subtitle',
            'category': self.category.id,
            'images': [self.image.id]
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_news_no_permission(self):
        """Test if a user without permissions can't update news"""
        data = {'title': 'Updated News Title'}
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_news_with_permission(self):
        """Test if a user with permission can update news"""
        data = {'title': 'Updated News Title'}
        permission = Permission.objects.get(codename='change_news')
        self.user.user_permissions.add(permission)
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_can_update_news(self):
        """Test if a superuser can update news"""
        data = {'title': 'Super Updated News Title'}
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_news_no_permission(self):
        """Test if a user without permissions can't delete news"""
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_news_with_permission(self):
        """Test if a user with permission can delete news"""
        permission = Permission.objects.get(codename='delete_news')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_superuser_can_delete_news(self):
        """Test if a superuser can delete news"""
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

