from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import Professor, Image, User
from BackendTennis.serializers import ProfessorDetailSerializer


class ProfessorViewTests(APITestCase):

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
        cls.api_key, cls.key = APIKey.objects.create_key(name='test-api-key')

        cls.image = Image.objects.create(title='Professor Image', type='professor')

        cls.professor = Professor.objects.create(
            fullName='Test Professor',
            image=cls.image,
            role='Test User',
            diploma='DE',
            best_rank='2/6'
        )
        cls.url = '/BackendTennis/professor/'
        cls.detail_url = f'{cls.url}{cls.professor.id}/'

    def test_get_professor_list(self):
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

        professors = Professor.objects.all()
        serializer = ProfessorDetailSerializer(professors, many=True)
        self.assertEqual(response.data['data'], serializer.data, str(response.data))
        self.assertEqual(response.data['status'], 'success', str(response.data))
        self.assertEqual(response.data['count'], len(serializer.data), str(response.data))

    def test_get_professor_detail(self):
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.assertEqual(response.data['fullName'], self.professor.fullName, str(response.data))

    def test_create_professor_with_jwt_and_api_key(self):
        data = {
            'fullName': 'New Professor',
            'image': self.image.id,
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6',
            'order': 2
        }
        permission = Permission.objects.get(codename='add_professor')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))
        self.assertEqual(Professor.objects.count(), 2, str(response.data))

    def test_create_professor_without_jwt(self):
        data = {'fullName': 'New Professor', 'image': self.image.id}
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_update_professor_with_jwt_and_api_key(self):
        data = {'fullName': 'Updated Professor'}
        permission = Permission.objects.get(codename='change_professor')
        self.user.user_permissions.add(permission)
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.professor.refresh_from_db()
        self.assertEqual(self.professor.fullName, 'Updated Professor', str(response.data))

    def test_delete_professor_with_jwt_and_api_key(self):
        permission = Permission.objects.get(codename='delete_professor')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(Professor.objects.count(), 0, str(response.data))

    def test_invalid_image_type_for_professor(self):
        invalid_image = Image.objects.create(title='Invalid Image', type='profile')
        data = {'fullName': 'Invalid Professor', 'image': invalid_image.id}
        permission = Permission.objects.get(codename='add_professor')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, str(response.data))
        self.assertIn('Image must be of type \'professor\'.', str(response.data))
