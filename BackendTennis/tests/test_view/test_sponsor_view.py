from datetime import date
from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken
from BackendTennis.models import Sponsor, Image, User
from BackendTennis.serializers import SponsorSerializer, SponsorDetailSerializer


class SponsorViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            birthdate=date(1990, 1, 1)
        )
        self.token = str(AccessToken.for_user(self.user))
        self.api_key, self.key = APIKey.objects.create_key(name="test-api-key")

        self.image = Image.objects.create(title='Sponsor Image', type='sponsor')

        self.sponsor = Sponsor.objects.create(brandName='Test Sponsor', image=self.image)
        self.url = '/BackendTennis/sponsor/'
        self.detail_url = f'{self.url}{self.sponsor.id}/'

    def test_get_sponsor_list(self):
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sponsors = Sponsor.objects.all()
        serializer = SponsorDetailSerializer(sponsors, many=True)
        print(response.data['data'])
        print(serializer.data)
        self.assertEqual(response.data['data'], serializer.data)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['count'], len(serializer.data))

    def test_get_sponsor_detail(self):
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['brandName'], self.sponsor.brandName)

    def test_create_sponsor_with_jwt_and_api_key(self):
        data = {'brandName': 'New Sponsor', 'image': self.image.id}
        permission = Permission.objects.get(codename='add_sponsor')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sponsor.objects.count(), 2)

    def test_create_sponsor_without_jwt(self):
        data = {'brandName': 'New Sponsor', 'image': self.image.id}
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_sponsor_with_jwt_and_api_key(self):
        data = {'brandName': 'Updated Sponsor'}
        permission = Permission.objects.get(codename='change_sponsor')
        self.user.user_permissions.add(permission)
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sponsor.refresh_from_db()
        self.assertEqual(self.sponsor.brandName, 'Updated Sponsor')

    def test_delete_sponsor_with_jwt_and_api_key(self):
        permission = Permission.objects.get(codename='delete_sponsor')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Sponsor.objects.count(), 0)

    def test_invalid_image_type_for_sponsor(self):
        invalid_image = Image.objects.create(title='Invalid Image', type='profile')
        data = {'brandName': 'Invalid Sponsor', 'image': invalid_image.id}
        permission = Permission.objects.get(codename='add_sponsor')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Image must be of type \'sponsor\'.', str(response.data))
