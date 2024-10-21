from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from BackendTennis.models import Category
from BackendTennis.serializers import CategorySerializer


class CategorySerializerTests(APITestCase):

    def setUp(self):
        self.valid_data = {
            'name': 'Tennis Category',
            'icon': 'icon.jpg'
        }

        self.category = Category.objects.create(
            name="Existing Category",
            icon="existing_icon.jpg"
        )

    def test_category_serializer_valid_data(self):
        """ Test serializer with valid data """
        serializer = CategorySerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], 'Tennis Category')

    def test_category_serializer_missing_name(self):
        """ Test serializer with missing name field """
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = ''  # Replace with empty string
        serializer = CategorySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)  # Ensure 'name' is flagged as invalid

    def test_category_serializer_missing_icon(self):
        """ Test serializer with missing icon field """
        invalid_data = self.valid_data.copy()
        invalid_data['icon'] = ''  # Replace with empty string
        serializer = CategorySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('icon', serializer.errors)  # Ensure 'icon' is flagged as invalid

    def test_create_category(self):
        """ Test creating a Category object through the serializer """
        serializer = CategorySerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertIsInstance(category, Category)
        self.assertEqual(category.name, 'Tennis Category')
        self.assertEqual(category.icon, 'icon.jpg')

    def test_update_category(self):
        """ Test updating an existing Category using the serializer """
        update_data = {'name': 'Updated Category'}
        serializer = CategorySerializer(self.category, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_category = serializer.save()
        self.assertEqual(updated_category.name, 'Updated Category')

    def test_partial_update_category_icon(self):
        """ Test partial update of the icon using the serializer """
        update_data = {'icon': 'updated_icon.jpg'}
        serializer = CategorySerializer(self.category, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_category = serializer.save()
        self.assertEqual(updated_category.icon, 'updated_icon.jpg')

    def test_invalid_icon_field(self):
        """ Test invalid icon field with a value that exceeds 1000 characters """
        invalid_data = self.valid_data.copy()
        invalid_data['icon'] = 'x' * 1001  # Invalid icon with more than 1000 characters
        serializer = CategorySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('icon', serializer.errors)

    def test_invalid_name_field(self):
        """ Test invalid name field with an empty value """
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = ''  # Invalid name (empty string)
        serializer = CategorySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
