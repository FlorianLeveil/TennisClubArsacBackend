from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey

from BackendTennis.models import User


class TestTokenView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            birthdate=date(1990, 1, 1)
        )

        cls.api_key, cls.key = APIKey.objects.create_key(name='test-api-key')

        cls.url = '/api/token/'

    def test_get_about_page_list_no_authentication(self):
        """ Test if unauthenticated users cannot access the token """
        data = {
            'email': self.user.email,
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data=data)
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response)
        self.assertIn('refresh', json_response)
        self.assertIn('access', json_response)
