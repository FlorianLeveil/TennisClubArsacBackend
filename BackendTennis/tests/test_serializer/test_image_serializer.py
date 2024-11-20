from rest_framework.test import APITestCase
from BackendTennis.models import Image, Tag
from BackendTennis.serializers import ImageSerializer
from BackendTennis.constant import Constant
from io import BytesIO
from PIL import Image as PilImage
from django.core.files.uploadedfile import SimpleUploadedFile


class ImageSerializerTests(APITestCase):

    def setUp(self):
        # Crée un objet Tag pour tester la relation avec Image
        self.tag = Tag.objects.create(name="Test Tag")

        # Création d'une image de test
        self.valid_image_file = self.generate_test_image()

        # Données valides pour créer une image
        self.valid_data = {
            'title': 'Test Image',
            'type': Constant.IMAGE_TYPE.SPONSOR,  # Supposons que ce type soit valide
            'tags': [self.tag.id],
            'imageUrl': self.valid_image_file
        }

    def generate_test_image(self):
        """ Helper method to generate a temporary image for testing """
        image = PilImage.new('RGB', (100, 100), color='blue')
        image_file = BytesIO()
        image.save(image_file, 'jpeg')
        image_file.seek(0)
        return SimpleUploadedFile('test_image.jpg', image_file.read(), content_type='image/jpeg')

    def test_image_serializer_with_valid_data(self):
        """ Teste la sérialisation d'une image avec des données valides """
        serializer = ImageSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        image = serializer.save()
        self.assertEqual(image.title, 'Test Image')
        self.assertEqual(image.type, Constant.IMAGE_TYPE.SPONSOR)
        self.assertEqual(image.tags.first().name, 'Test Tag')

    def test_image_serializer_missing_required_fields(self):
        """ Teste la validation lorsque des champs obligatoires sont manquants """
        invalid_data = {
            'title': 'Missing Type',
            # 'type' est manquant
            'tags': [self.tag.id]
        }
        serializer = ImageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('type', serializer.errors)

    def test_image_serializer_invalid_type(self):
        """ Teste la validation du type d'image invalide """
        invalid_data = self.valid_data.copy()
        invalid_data['type'] = 'invalid_type'
        serializer = ImageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('type', serializer.errors)

    def test_image_serializer_update(self):
        """ Teste la mise à jour d'une image existante """
        image = Image.objects.create(title='Old Title', type=Constant.IMAGE_TYPE.SPONSOR)
        update_data = {
            'title': 'Updated Title',
            'tags': [self.tag.id]
        }
        serializer = ImageSerializer(instance=image, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_image = serializer.save()
        self.assertEqual(updated_image.title, 'Updated Title')
        self.assertEqual(updated_image.tags.first().name, 'Test Tag')

    def test_image_serializer_create_with_tags(self):
        """ Teste la création d'une image avec des tags associés """
        serializer = ImageSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        image = serializer.save()
        self.assertEqual(image.tags.count(), 1)
        self.assertEqual(image.tags.first().name, 'Test Tag')

    def test_image_serializer_missing_image_file(self):
        """ Teste la validation lorsque le champ imageUrl est manquant """
        invalid_data = self.valid_data.copy()
        invalid_data.pop('imageUrl')  # Retirer l'image
        serializer = ImageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('imageUrl', serializer.errors)

    def test_image_serializer_valid_imageUrlLink(self):
        """ Teste si le lien de l'image est correctement généré """
        image = Image.objects.create(
            title='Test Image',
            type=Constant.IMAGE_TYPE.SPONSOR,
            imageUrl=self.valid_image_file
        )
        serializer = ImageSerializer(instance=image)
        self.assertEqual(serializer.data['imageUrlLink'], image.imageUrl.url)

    def test_image_serializer_no_tags(self):
        """ Teste la création d'une image sans tags associés """
        valid_data_no_tags = self.valid_data.copy()
        valid_data_no_tags.pop('tags')
        serializer = ImageSerializer(data=valid_data_no_tags)
        self.assertTrue(serializer.is_valid())
        image = serializer.save()
        self.assertEqual(image.tags.count(), 0)
