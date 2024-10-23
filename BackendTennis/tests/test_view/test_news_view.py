from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken

from BackendTennis.models import News, Category, User, Image
from BackendTennis.serializers import NewsSerializer


class NewsViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            birthdate='1990-01-01',
            is_superuser=True
        )

        cls.token = str(AccessToken.for_user(cls.user))

        cls.api_key, cls.key = APIKey.objects.create_key(name="test-api-key")

        cls.category = Category.objects.create(name="Sport")

        cls.image = Image.objects.create(type='news', imageUrl='test_image.jpg')

        cls.news = News.objects.create(
            title='Test News',
            content='This is a test news content.',
            subtitle='Test Subtitle',
            category=cls.category
        )
        cls.news.images.add(cls.image)

        cls.url = '/BackendTennis/news/'
        cls.detail_url = f'{cls.url}{cls.news.id}/'

    def test_get_news_list(self):
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        self.assertEqual(response.data['data'], serializer.data)
        self.assertEqual(response.data['status'], 'success')

    def test_get_news_detail(self):
        response = self.client.get(self.detail_url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.news.title)

    def test_create_news(self):
        data = {
            'title': 'New Test News',
            'content': 'New test news content.',
            'subtitle': 'New Test Subtitle',
            'category': self.category.id,
            'images': [self.image.id]
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_news(self):
        update_data = {
            'title': 'Updated News Title',
            'content': 'Updated news content.'
        }
        response = self.client.patch(
            self.detail_url,
            data=update_data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.news.refresh_from_db()
        self.assertEqual(self.news.title, 'Updated News Title')

    def test_delete_news(self):
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(News.objects.count(), 0)

    def test_create_news_without_jwt(self):
        data = {
            'title': 'Unauthorized News',
            'content': 'Unauthorized content.',
            'subtitle': 'Unauthorized Subtitle',
            'category': self.category.id,
            'images': [self.image.id]
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_news_with_invalid_data(self):
        data = {
            'title': '',  # Titre manquant
            'content': 'Content with missing title.',
            'subtitle': 'Invalid Subtitle',
            'category': self.category.id,
            'images': [self.image.id]
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data['data'])

    def test_update_news_with_invalid_data(self):
        update_data = {
            'title': ''  # Titre manquant
        }
        response = self.client.patch(
            self.detail_url,
            data=update_data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data['data'])
