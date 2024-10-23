from datetime import datetime, date

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import User, Tournament


class TournamentSerializerTestCase(APITestCase):

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

        cls.tournament = Tournament.objects.create(
            name='Test Tournament',
            unregisteredParticipants=[],
            cancel=False,
            start=datetime(2024, 10, 12),
            end=datetime(2024, 10, 13)
        )
        cls.tournament.participants.set([cls.user.id])

        cls.url = '/BackendTennis/tournament/'
        cls.detail_url = f'{cls.url}{cls.tournament.id}/'

    def test_get_tournament_list_no_authentication(self):
        """ Test if unauthenticated users cannot access the tournament list """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_tournament_list_with_api_key(self):
        """ Test if users with API key can access the tournament list """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tournament_list_with_start_date_only_1_tournament(self):
        """ Test filtering tournaments by start_date """
        _date = datetime(2024, 10, 11)
        response = self.client.get(f'{self.url}?start_date={_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['data'][0]['name'], "Test Tournament")

    def test_get_tournament_list_with_start_date_only_0_tournament(self):
        """ Test filtering tournaments by start_date """
        _date = datetime(2024, 10, 14)
        response = self.client.get(f'{self.url}?start_date={_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_get_tournament_list_with_end_date_only_1_tournament(self):
        """ Test filtering tournaments by end_date """
        _date = datetime(2024, 10, 14)
        response = self.client.get(f'{self.url}?end_date={_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['data'][0]['name'], "Test Tournament")

    def test_get_tournament_list_with_end_date_only_0_tournament(self):
        """ Test filtering tournaments by end_date """
        _date = datetime(2024, 10, 10)
        response = self.client.get(f'{self.url}?end_date={_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_get_tournament_list_with_star_date_end_date_1_tournament(self):
        """ Test filtering tournaments by start_date and end_date """
        start_date = datetime(2024, 10, 10)
        end_date = datetime(2024, 10, 15)
        response = self.client.get(f'{self.url}?start_date={start_date}&end_date={end_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['data'][0]['name'], "Test Tournament")

    def test_get_tournament_list_with_start_date_end_date_0_tournament(self):
        """ Test filtering tournaments by start_date and end_date """
        start_date = datetime(2024, 10, 15)
        end_date = datetime(2024, 10, 16)
        response = self.client.get(f'{self.url}?start_date={start_date}&end_date={end_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_create_tournament_no_permission(self):
        data = {
            'name': 'Test Tournament',
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
            'start': datetime(2024, 10, 12),
            'end': datetime(2024, 10, 13),
        }
        """ Test creating a tournament without permission """
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_tournament_with_permission(self):
        """ Test creating a tournament with correct permissions """
        data = {
            'name': 'Test Tournament',
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
            'start': datetime(2024, 10, 12),
            'end': datetime(2024, 10, 13),
        }
        permission = Permission.objects.get(codename='add_tournament')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tournament_detail_with_api_key(self):
        """ Test retrieving a tournament detail """
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.tournament.name)

    def test_update_tournament_no_permission(self):
        """ Test updating a tournament without permission """
        data = {'name': 'Updated Tournament'}
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_tournament_with_permission(self):
        """ Test updating a tournament with correct permissions """
        data = {'name': 'Updated Tournament'}
        permission = Permission.objects.get(codename='change_tournament')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tournament.refresh_from_db()
        self.assertEqual(self.tournament.name, 'Updated Tournament')

    def test_delete_tournament_no_permission(self):
        """ Test deleting a tournament without permission """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_tournament_with_permission(self):
        """ Test deleting a tournament with correct permissions """
        permission = Permission.objects.get(codename='delete_tournament')
        self.user.user_permissions.add(permission)
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tournament.objects.count(), 0)

    def test_superuser_can_create_tournament(self):
        """ Test if a superuser can create a tournament """
        data = {
            'name': 'Test Tournament',
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
            'start': datetime(2024, 10, 12),
            'end': datetime(2024, 10, 13),
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key,
                                    HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superuser_can_update_tournament(self):
        """ Test if a superuser can update a tournament """
        data = {'name': 'Superuser Updated Tournament'}
        response = self.client.patch(self.detail_url, data=data, HTTP_API_KEY=self.key,
                                     HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tournament.refresh_from_db()
        self.assertEqual(self.tournament.name, 'Superuser Updated Tournament')

    def test_superuser_can_delete_tournament(self):
        """ Test if a superuser can delete a tournament """
        response = self.client.delete(self.detail_url, HTTP_API_KEY=self.key,
                                      HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tournament.objects.count(), 0)
