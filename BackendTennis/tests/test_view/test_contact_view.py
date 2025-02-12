from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey


class TestContactView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_key, cls.key = APIKey.objects.create_key(name="test-api-key")
        cls.url = '/BackendTennis/contact/'

    def test_send_mail__successfully(self):
        """ Test sending an email """
        data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'phone_number': '0601020304',
            'email': 'john_doe@test.com',
            'subject': 'Test mail',
            'message': 'This mail is a test',
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.data))

    def test_send_mail__firstname_to_long(self):
        data = {
            'firstname': 'John' * 100,
            'lastname': 'Doe',
            'phone_number': '0601020304',
            'email': 'john_doe@test.com',
            'subject': 'Test mail',
            'message': 'This mail is a test',
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, str(response.data))
        self.assertIn('firstname', response.data, 'No error on firstname, need max_length error.')
        self.assertEqual(
            response.data['firstname'][0],
            'The Firstname must not exceed 40 characters.'
        )

    def test_send_mail__lastname_to_long(self):
        data = {
            'firstname': 'John',
            'lastname': 'Doe' * 100,
            'phone_number': '0601020304',
            'email': 'john_doe@test.com',
            'subject': 'Test mail',
            'message': 'This mail is a test',
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, str(response.data))
        self.assertIn('lastname', response.data, 'No error on lastname, need max_length error.')
        self.assertEqual(
            response.data['lastname'][0],
            'The Lastname must not exceed 40 characters.'
        )

    def test_send_mail__phone_number_wrong_format(self):
        data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'phone_number': '0333',
            'email': 'john_doe@test.com',
            'subject': 'Test mail',
            'message': 'This mail is a test',
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, str(response.data))
        self.assertIn('phone_number', response.data, 'No error on phone_number, need format error.')
        self.assertEqual(
            response.data['phone_number'][0],
            'Enter a valid phone number.'
        )

    def test_send_mail__email_wrong_format(self):
        data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'phone_number': '0601020304',
            'email': 'john_doe',
            'subject': 'Test mail',
            'message': 'This mail is a test',
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, str(response.data))
        self.assertIn('email', response.data, 'No error on email, need format error.')
        self.assertEqual(
            response.data['email'][0],
            'The Email address must be in a valid format (ex: <ADDRESS>@<DOMAIN>.com).'
        )

    def test_send_mail__subject_too_long(self):
        data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'phone_number': '0601020304',
            'email': 'john_doe@test.com',
            'subject': 'Test mail' * 100,
            'message': 'This mail is a test',
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, str(response.data))
        self.assertIn('subject', response.data, 'No error on subject, need max_length error.')
        self.assertEqual(
            response.data['subject'][0],
            'The Subject must not exceed 180 characters.'
        )

    def test_send_mail__message_too_long(self):
        data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'phone_number': '0601020304',
            'email': 'john_doe@test.com',
            'subject': 'Test mail',
            'message': 'This mail is a test' * 1000,
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, str(response.data))
        self.assertIn('message', response.data, 'No error on message, need max_length error.')
        self.assertEqual(
            response.data['message'][0],
            'The Message must not exceed 1000 characters.'
        )
