from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import Tag, User
from BackendTennis.serializers import TagSerializer


class TagViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            birthdate=date(1990, 1, 1)
        )

        cls.token = str(AccessToken.for_user(cls.user))

        cls.api_key, cls.key = APIKey.objects.create_key(name="test-api-key")
        cls.tag = Tag.objects.create(name='Test Tag')
        cls.url = '/BackendTennis/tag/'
        cls.detail_url = f'{cls.url}{cls.tag.id}/'

    def test_get_tag_list(self):
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.data['data'], serializer.data)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['count'], len(serializer.data))

    def test_get_tag_list_with_api_key(self):
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_get_tag_list_with_invalid_api_key(self):
        response = self.client.get(self.url, HTTP_API_KEY="invalid_key")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_tag_with_jwt_and_api_key(self):
        data = {'name': 'New Tag'}
        permission = Permission.objects.get(codename='add_tag')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_tag_without_jwt(self):
        data = {'name': 'New Tag'}
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_tag_detail_with_api_key(self):
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.tag.name)

    def test_update_tag_with_jwt_and_api_key(self):
        data = {'name': 'Updated tag'}
        permission = Permission.objects.get(codename='change_tag')
        self.user.user_permissions.add(permission)
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, 'Updated tag')

    def test_delete_tag_with_jwt_and_api_key(self):
        permission = Permission.objects.get(codename='delete_tag')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 0)
