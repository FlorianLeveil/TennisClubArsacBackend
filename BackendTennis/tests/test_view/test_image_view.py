import os.path
from pathlib import Path
from datetime import datetime, date, timedelta
from io import BytesIO

from PIL import Image as PilImage
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.constant import Constant
from BackendTennis.models import User, Image


class ImageViewTests(APITestCase):

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

        cls.image = Image.objects.create(type=Constant.IMAGE_TYPE.SPONSOR, imageUrl='test_image_url.jpg')
        cls.url = '/BackendTennis/image/'
        cls.multi_url = '/BackendTennis/images/'
        cls.detail_url = f'{cls.url}{cls.image.id}/'

    @staticmethod
    def get_delete_image_path(image: Image) -> Path:
        today = date.today()
        project_root = Path(__file__).parent.parent.parent.parent.resolve()
        return Path(
            project_root,
            'images_deleted',
            str(today.year),
            str(today.month),
            str(today.day),
            f'{image.id}.{str(image.imageUrl).split('.')[-1]}'
        )

    @staticmethod
    def create_test_image_file(image_id: str):
        image = PilImage.new('RGB', (100, 100), color='red')
        image_file = BytesIO()
        image.save(image_file, 'jpeg')
        image_file.seek(0)
        return SimpleUploadedFile(f'{image_id}.jpg', image_file.read(), content_type='image/jpeg')

    def create_image_object(self) -> Image:
        image = Image.objects.create(type=Constant.IMAGE_TYPE.SPONSOR)
        image_url = self.create_test_image_file(str(image.id))
        image.imageUrl = image_url
        image.save()
        return image

    def test_get_image_list_no_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_image_list_with_api_key(self):
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_image_list_filtered_by_type(self):
        Image.objects.create(type=Constant.IMAGE_TYPE.NEWS, imageUrl='news_image.jpg')
        response = self.client.get(f'{self.url}?type={Constant.IMAGE_TYPE.NEWS}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['data'][0]['type'], Constant.IMAGE_TYPE.NEWS)

    def test_get_image_list_filtered_by_date_range(self):
        Image.objects.all().delete()
        start_date = (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y')
        end_date = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
        Image.objects.create(type=Constant.IMAGE_TYPE.EVENT, imageUrl='event_image.jpg')
        response = self.client.get(f'{self.url}?start={start_date}&end={end_date}', HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_image_no_permission(self):
        image_file = self.create_test_image_file('test')
        data = {
            'type': Constant.IMAGE_TYPE.SPONSOR,
            'imageUrl': image_file
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_image_with_permission(self):
        image_file = self.create_test_image_file('test')
        data = {
            'title': 'test',
            'type': Constant.IMAGE_TYPE.SPONSOR,
            'imageUrl': image_file
        }
        permission = Permission.objects.get(codename='add_image')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}',
                                    HTTP_API_KEY=self.key, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('imageUrlLink', response.data)

    def test_superuser_can_create_image(self):
        image_file = self.create_test_image_file('test')
        data = {
            'title': 'test',
            'type': Constant.IMAGE_TYPE.SPONSOR,
            'imageUrl': image_file
        }
        response = self.client.post(self.url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
                                    HTTP_API_KEY=self.key, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_image_no_permission(self):
        image_file = self.create_test_image_file('test')
        data = {'imageUrl': image_file}
        response = self.client.patch(self.detail_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}',
                                     HTTP_API_KEY=self.key, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_image_with_permission(self):
        image_file = self.create_test_image_file('test')
        data = {'imageUrl': image_file}
        permission = Permission.objects.get(codename='change_image')
        self.user.user_permissions.add(permission)
        response = self.client.patch(self.detail_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}',
                                     HTTP_API_KEY=self.key, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.image.refresh_from_db()
        self.assertTrue(self.image.imageUrl.url.endswith('.jpg'))

    def test_superuser_can_update_image(self):
        image_file = self.create_test_image_file('test')
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

    def test_delete_multiple_images_with_permission(self):
        image1 = self.create_image_object()
        image2 = self.create_image_object()
        image3 = self.create_image_object()
        image4 = self.create_image_object()
        image5 = self.create_image_object()
        data = {'ids': [image1.id, image2.id, image3.id, image4.id, image5.id]}
        all_images = list(Image.objects.all().values_list('id', flat=True))
        self.assertIn(image1.id, all_images, 'Image "image1" not saved')
        self.assertIn(image2.id, all_images, 'Image "image2" not saved')
        self.assertIn(image3.id, all_images, 'Image "image3" not saved')
        self.assertIn(image4.id, all_images, 'Image "image4" not saved')
        self.assertIn(image5.id, all_images, 'Image "image5" not saved')

        permission = Permission.objects.get(codename='delete_image')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.multi_url,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('success', False), True)
        all_images = list(Image.objects.all().values_list('id', flat=True))
        self.assertNotIn(image1.id, all_images, 'Image "image1" not deleted')
        self.assertNotIn(image2.id, all_images, 'Image "image2" not deleted')
        self.assertNotIn(image3.id, all_images, 'Image "image3" not deleted')
        self.assertNotIn(image4.id, all_images, 'Image "image4" not deleted')
        self.assertNotIn(image5.id, all_images, 'Image "image5" not deleted')

        self.assertTrue(self.get_delete_image_path(image1).exists(), 'Image "image1" not present in Delete directory')
        self.assertTrue(self.get_delete_image_path(image2).exists(), 'Image "image2" not present in Delete directory')
        self.assertTrue(self.get_delete_image_path(image3).exists(), 'Image "image3" not present in Delete directory')
        self.assertTrue(self.get_delete_image_path(image4).exists(), 'Image "image4" not present in Delete directory')
        self.assertTrue(self.get_delete_image_path(image5).exists(), 'Image "image5" not present in Delete directory')

    def test_superuser_can_delete_multiple_images(self):
        image1 = self.create_image_object()
        image2 = self.create_image_object()
        image3 = self.create_image_object()
        image4 = self.create_image_object()
        image5 = self.create_image_object()
        data = {'ids': [image1.id, image2.id, image3.id, image4.id, image5.id]}
        all_images = list(Image.objects.all().values_list('id', flat=True))
        self.assertIn(image1.id, all_images, 'Image "image1" not saved')
        self.assertIn(image2.id, all_images, 'Image "image2" not saved')
        self.assertIn(image3.id, all_images, 'Image "image3" not saved')
        self.assertIn(image4.id, all_images, 'Image "image4" not saved')
        self.assertIn(image5.id, all_images, 'Image "image5" not saved')

        response = self.client.delete(
            self.multi_url,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            data=data,
            HTTP_API_KEY=self.key
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('success', False), True)
        all_images = list(Image.objects.all().values_list('id', flat=True))
        self.assertNotIn(image1.id, all_images, 'Image "image1" not deleted')
        self.assertNotIn(image2.id, all_images, 'Image "image2" not deleted')
        self.assertNotIn(image3.id, all_images, 'Image "image3" not deleted')
        self.assertNotIn(image4.id, all_images, 'Image "image4" not deleted')
        self.assertNotIn(image5.id, all_images, 'Image "image5" not deleted')

        self.assertTrue(self.get_delete_image_path(image1).exists(), 'Image "image1" not present in Delete directory')
        self.assertTrue(self.get_delete_image_path(image2).exists(), 'Image "image2" not present in Delete directory')
        self.assertTrue(self.get_delete_image_path(image3).exists(), 'Image "image3" not present in Delete directory')
        self.assertTrue(self.get_delete_image_path(image4).exists(), 'Image "image4" not present in Delete directory')
        self.assertTrue(self.get_delete_image_path(image5).exists(), 'Image "image5" not present in Delete directory')

    def test_get_image_detail(self):
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('imageUrlLink', response.data)
        self.assertTrue(response.data['imageUrlLink'].endswith('.jpg'))
