from rest_framework.test import APITestCase

from BackendTennis.models import ClubValue
from BackendTennis.serializers import ClubValueSerializer


class ClubValueSerializerTests(APITestCase):

    def setUp(self):
        self.valid_data = {
            'title': 'Tennis ClubValue',
            'description': 'Tennis ClubValue description',
            'order': 1
        }

        self.club_value = ClubValue.objects.create(
            title='ClubValue Title',
            description='ClubValue description',
            order=0
        )

    def test_club_value_serializer_valid_data(self):
        """ Test serializer with valid data """
        serializer = ClubValueSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['title'], 'Tennis ClubValue')

    def test_club_value_serializer_missing_title(self):
        """ Test serializer with missing title field """
        invalid_data = self.valid_data.copy()
        invalid_data['title'] = ''  # Replace with empty string
        serializer = ClubValueSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)  # Ensure 'title' is flagged as invalid

    def test_club_value_serializer_missing_description(self):
        """ Test serializer with missing description field """
        invalid_data = self.valid_data.copy()
        invalid_data['description'] = ''  # Replace with empty string
        serializer = ClubValueSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)  # Ensure 'description' is flagged as invalid

    def test_club_value_serializer_missing_order(self):
        """ Test serializer with missing order field """
        invalid_data = self.valid_data.copy()
        invalid_data['order'] = ''  # Replace with empty string
        serializer = ClubValueSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('order', serializer.errors)  # Ensure 'order' is flagged as invalid

    def test_create_club_value(self):
        """ Test creating a ClubValue object through the serializer """
        serializer = ClubValueSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        club_value = serializer.save()
        self.assertIsInstance(club_value, ClubValue)
        self.assertEqual(club_value.title, 'Tennis ClubValue')
        self.assertEqual(club_value.description, 'Tennis ClubValue description')

    def test_update_club_value(self):
        """ Test updating an existing ClubValue using the serializer """
        update_data = {'title': 'Updated ClubValue'}
        serializer = ClubValueSerializer(self.club_value, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_club_value = serializer.save()
        self.assertEqual(updated_club_value.title, 'Updated ClubValue')

    def test_partial_update_club_value_description(self):
        """ Test partial update of the description using the serializer """
        update_data = {'description': 'ClubValue description Updated'}
        serializer = ClubValueSerializer(self.club_value, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_club_value = serializer.save()
        self.assertEqual(updated_club_value.description, 'ClubValue description Updated')

    def test_partial_update_club_value_order(self):
        """ Test partial update of the description using the serializer """
        update_data = {'order': 3}
        serializer = ClubValueSerializer(self.club_value, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_club_value = serializer.save()
        self.assertEqual(updated_club_value.order, 3)

    def test_invalid_title_field(self):
        """ Test invalid title field with an empty value """
        invalid_data = self.valid_data.copy()
        invalid_data['title'] = ''  # Invalid title (empty string)
        serializer = ClubValueSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_invalid_order_field(self):
        """ Test invalid title field with an empty value """
        invalid_data = self.valid_data.copy()
        invalid_data['order'] = 0  # Invalid title (already exist)
        serializer = ClubValueSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('order', serializer.errors)
