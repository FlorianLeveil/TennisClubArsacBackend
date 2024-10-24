from datetime import date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import TeamMember, Image, User
from BackendTennis.serializers import TeamMemberDetailSerializer


class TeamMemberViewTests(APITestCase):

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

        cls.image = Image.objects.create(title='TeamMember Image', type='team_member')

        cls.team_member = TeamMember.objects.create(
            fullName='Test Team Member',
            image=cls.image,
            role='Test User',
            description='test description'
        )
        cls.url = '/BackendTennis/team_member/'
        cls.detail_url = f'{cls.url}{cls.team_member.id}/'

    def test_get_team_member_list(self):
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

        team_members = TeamMember.objects.all()
        serializer = TeamMemberDetailSerializer(team_members, many=True)
        self.assertEqual(response.data['data'], serializer.data, str(response.data))
        self.assertEqual(response.data['status'], 'success', str(response.data))
        self.assertEqual(response.data['count'], len(serializer.data), str(response.data))

    def test_get_team_member_detail(self):
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.assertEqual(response.data['fullName'], self.team_member.fullName, str(response.data))

    def test_create_team_member_with_jwt_and_api_key(self):
        data = {
            'fullName': 'New TeamMember',
            'image': self.image.id,
            'role': 'Test User',
            'description': 'test description'
        }
        permission = Permission.objects.get(codename='add_teammember')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.data))
        self.assertEqual(TeamMember.objects.count(), 2, str(response.data))

    def test_create_team_member_without_jwt(self):
        data = {'fullName': 'New TeamMember', 'image': self.image.id}
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, str(response.data))

    def test_update_team_member_with_jwt_and_api_key(self):
        data = {'fullName': 'Updated TeamMember'}
        permission = Permission.objects.get(codename='change_teammember')
        self.user.user_permissions.add(permission)
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))
        self.team_member.refresh_from_db()
        self.assertEqual(self.team_member.fullName, 'Updated TeamMember', str(response.data))

    def test_delete_team_member_with_jwt_and_api_key(self):
        permission = Permission.objects.get(codename='delete_teammember')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, str(response.data))
        self.assertEqual(TeamMember.objects.count(), 0, str(response.data))

    def test_invalid_image_type_for_team_member(self):
        invalid_image = Image.objects.create(title='Invalid Image', type='profile')
        data = {'fullName': 'Invalid TeamMember', 'image': invalid_image.id}
        permission = Permission.objects.get(codename='add_teammember')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, str(response.data))
        self.assertIn('Image must be of type \'team_member\'.', str(response.data))
