import io
from PIL import Image as PilImage
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, date, timedelta
from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken
from BackendTennis.models import User, Image
from BackendTennis.constant import Constant


class ImageViewTests(APITestCase):

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
        self.token = str(AccessToken.for_user(self.user))
        self.superuser_token = str(AccessToken.for_user(self.superuser))

        self.image = Image.objects.create(type=Constant.IMAGE_TYPE.SPONSOR, imageUrl="test_image_url.jpg")
        self.url = '/BackendTennis/image/'
        self.detail_url = f'{self.url}{self.image.id}/'

    def create_test_image_file(self):
        image = PilImage.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        return SimpleUploadedFile('test_image.jpg', image_file.read(), content_type='image/jpeg')

    def test_get_image_list_no_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_image_list_with_api_key(self):
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_image_list_filtered_by_type(self):
        Image.objects.create(type=Constant.IMAGE_TYPE.NEWS, imageUrl="news_image.jpg")
        response = self.client.get(f'{self.url}?type={Constant.IMAGE_TYPE.NEWS}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['data'][0]['type'], Constant.IMAGE_TYPE.NEWS)

    def test_get_image_list_filtered_by_date_range(self):
        Image.objects.all().delete()
        start_date = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")
        end_date = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
        Image.objects.create(type=Constant.IMAGE_TYPE.EVENT, imageUrl="event_image.jpg")
        response = self.client.get(f'{self.url}?start={start_date}&end={end_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_image_no_permission(self):
        image_file = self.create_test_image_file()
        data = {
            'type': Constant.IMAGE_TYPE.SPONSOR,
            'imageUrl': image_file
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_image_with_permission(self):
        image_file = self.create_test_image_file()
        data = {
            'title': 'test',
            'type': Constant.IMAGE_TYPE.SPONSOR,
            'imageUrl': image_file
        }
        permission = Permission.objects.get(codename='add_image')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}',
                                    HTTP_API_KEY=self.key, format='multipart')
        print(response.__str__())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('imageUrlLink', response.data)

    def test_superuser_can_create_image(self):
        image_file = self.create_test_image_file()
        data = {
            'title': 'test',
            'type': Constant.IMAGE_TYPE.SPONSOR,
            'imageUrl': image_file
        }
        response = self.client.post(self.url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
                                    HTTP_API_KEY=self.key, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_image_no_permission(self):
        image_file = self.create_test_image_file()
        data = {'imageUrl': image_file}
        response = self.client.patch(self.detail_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}',
                                     HTTP_API_KEY=self.key, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_image_with_permission(self):
        image_file = self.create_test_image_file()
        data = {'imageUrl': image_file}
        permission = Permission.objects.get(codename='change_image')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}',
                                     HTTP_API_KEY=self.key, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.image.refresh_from_db()
        self.assertTrue(self.image.imageUrl.url.endswith('.jpg'))

    def test_superuser_can_update_image(self):
        image_file = self.create_test_image_file()
        data = {'imageUrl': image_file}
        response = self.client.patch(self.detail_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
                                     HTTP_API_KEY=self.key, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.image.refresh_from_db()
        self.assertTrue(self.image.imageUrl.url.endswith('.jpg'))

    def test_delete_image_no_permission(self):
        response = self.client.delete(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.token}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_image_with_permission(self):
        permission = Permission.objects.get(codename='delete_image')
        self.user.user_permissions.add(permission)
        response = self.client.delete(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.token}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_superuser_can_delete_image(self):
        response = self.client.delete(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
                                      HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_image_detail(self):
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('imageUrlLink', response.data)
        self.assertTrue(response.data['imageUrlLink'].endswith('.jpg'))
