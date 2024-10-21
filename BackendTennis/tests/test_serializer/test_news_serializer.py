from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from BackendTennis.models import News, Category, Image
from BackendTennis.serializers import NewsSerializer


class NewsSerializerTestCase(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Sport')
        self.image1 = Image.objects.create(type='news', imageUrl='test_image1.jpg')
        self.image2 = Image.objects.create(type='news', imageUrl='test_image2.jpg')

        self.valid_data = {
            'title': 'Test News Title',
            'content': 'This is the content of the news.',
            'subtitle': 'Test News Subtitle',
            'category': self.category.id,
            'images': [self.image1.id, self.image2.id]
        }

        self.news = News.objects.create(
            title='Existing News',
            content='This is the content of the existing news.',
            subtitle='Existing News Subtitle',
            category=self.category
        )
        self.news.images.add(self.image1, self.image2)

    def test_news_serializer_with_valid_data(self):
        serializer = NewsSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['title'], 'Test News Title')

    def test_news_serializer_with_missing_fields(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop('title')  # Supprime le champ 'title'
        serializer = NewsSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_news_serializer_with_empty_title(self):
        invalid_data = self.valid_data.copy()
        invalid_data['title'] = ''  # Titre vide
        serializer = NewsSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_news_serializer_with_invalid_image(self):
        invalid_data = self.valid_data.copy()
        invalid_data['images'] = [9999]  # ID d'image non existant
        serializer = NewsSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('images', serializer.errors)

    def test_create_news(self):
        serializer = NewsSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        news = serializer.save()
        self.assertIsInstance(news, News)
        self.assertEqual(news.title, 'Test News Title')
        self.assertEqual(news.images.count(), 2)

    def test_update_news(self):
        update_data = {
            'title': 'Updated News Title',
            'content': 'Updated content.',
            'images': [self.image2.id]  # Remplace les images
        }
        serializer = NewsSerializer(self.news, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_news = serializer.save()
        self.assertEqual(updated_news.title, 'Updated News Title')
        self.assertEqual(updated_news.content, 'Updated content.')
        self.assertEqual(updated_news.images.count(), 1)

    def test_update_news_without_category(self):
        update_data = {
            'title': 'Updated News Title'
        }
        serializer = NewsSerializer(self.news, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_news = serializer.save()
        self.assertEqual(updated_news.category, self.category)

    def test_create_news_with_missing_category(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop('category')  # Catégorie manquante
        serializer = NewsSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('category', serializer.errors)

    def test_news_serializer_category_not_exist(self):
        invalid_data = self.valid_data.copy()
        invalid_data['category'] = 9999  # Catégorie inexistante
        serializer = NewsSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('category', serializer.errors)

    def test_create_news_with_no_images(self):
        data_no_images = self.valid_data.copy()
        data_no_images['images'] = []  # Pas d'images
        serializer = NewsSerializer(data=data_no_images)
        self.assertTrue(serializer.is_valid())
        news = serializer.save()
        self.assertEqual(news.images.count(), 0)

    def test_update_news_with_no_images(self):
        update_data = {
            'images': []  # Suppression des images
        }
        serializer = NewsSerializer(self.news, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_news = serializer.save()
        self.assertEqual(updated_news.images.count(), 0)

    def test_update_news_with_invalid_data(self):
        invalid_data = {
            'title': '',  # Titre vide
            'content': ''  # Contenu vide
        }
        serializer = NewsSerializer(self.news, data=invalid_data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        self.assertIn('content', serializer.errors)

    def test_news_serializer_with_too_long_content(self):
        invalid_data = self.valid_data.copy()
        invalid_data['content'] = 'A' * 2001
        serializer = NewsSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('content', serializer.errors)
