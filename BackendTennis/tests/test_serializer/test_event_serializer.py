from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from BackendTennis.models import Event, Image, Category
from BackendTennis.serializers import EventSerializer
from uuid import uuid4


class EventSerializerTests(APITestCase):

    def setUp(self):
        self.image = Image.objects.create(type='event', imageUrl='test_image_url.jpg')
        self.category = Category.objects.create(name='Test Category')

        self.valid_data = {
            'title': 'Test Event',
            'description': 'This is a test event.',
            'dateType': 'Single Day',
            'start': (datetime.now() + timedelta(days=1)).isoformat(),
            'end': (datetime.now() + timedelta(days=2)).isoformat(),
            'image': self.image.id,
            'category': self.category.id,
        }

    def test_event_serializer_with_valid_data(self):
        """ Test the serializer with valid data """
        serializer = EventSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['title'], 'Test Event')

    def test_event_serializer_missing_required_fields(self):
        """ Test the serializer with missing required fields """
        invalid_data = self.valid_data.copy()
        invalid_data.pop('title')  # Remove title to make data invalid

        serializer = EventSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_event_serializer_invalid_start_end_dates(self):
        """ Test the serializer with start date after end date """
        invalid_data = self.valid_data.copy()
        invalid_data['start'] = (datetime.now() + timedelta(days=3)).isoformat()
        invalid_data['end'] = (datetime.now() + timedelta(days=2)).isoformat()  # End is before start

        serializer = EventSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), "Start date must be before end date.")

    def test_event_serializer_create(self):
        """ Test creating a new event using the serializer """
        serializer = EventSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        event = serializer.save()
        self.assertIsInstance(event, Event)
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.image, self.image)
        self.assertEqual(event.category, self.category)

    def test_event_serializer_update(self):
        """ Test updating an existing event using the serializer """
        # Créer un événement en utilisant une instance d'image et de catégorie (au lieu d'un UUID)
        event = Event.objects.create(
            title=self.valid_data['title'],
            description=self.valid_data['description'],
            dateType=self.valid_data['dateType'],
            start=self.valid_data['start'],
            end=self.valid_data['end'],
            image=self.image,  # Utilisez l'instance d'image
            category=self.category  # Utilisez l'instance de catégorie
        )

        # Données de mise à jour
        update_data = {'title': 'Updated Event Title'}

        # Sérialisation et validation des données de mise à jour
        serializer = EventSerializer(event, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())

        # Mise à jour de l'événement
        updated_event = serializer.save()

        # Vérification que la mise à jour a bien eu lieu
        self.assertEqual(updated_event.title, 'Updated Event Title')

    def test_event_serializer_invalid_image(self):
        """ Test the serializer with an invalid image """
        invalid_data = self.valid_data.copy()
        invalid_data['image'] = uuid4()  # Invalid UUID for image

        serializer = EventSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('image', serializer.errors)

    def test_event_serializer_invalid_category(self):
        """ Test the serializer with an invalid category """
        invalid_data = self.valid_data.copy()
        invalid_data['category'] = uuid4()  # Invalid UUID for category

        serializer = EventSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('category', serializer.errors)

    def test_event_serializer_partial_update(self):
        """ Test partial update with the serializer """
        # Créer un événement en utilisant une instance d'image et de catégorie (au lieu d'un UUID)
        event = Event.objects.create(
            title=self.valid_data['title'],
            description=self.valid_data['description'],
            dateType=self.valid_data['dateType'],
            start=self.valid_data['start'],
            end=self.valid_data['end'],
            image=self.image,  # Utilisez l'instance d'image
            category=self.category  # Utilisez l'instance de catégorie
        )

        # Données partielles à mettre à jour
        partial_data = {'description': 'Updated description.'}

        # Sérialisation et validation des données partielles
        serializer = EventSerializer(event, data=partial_data, partial=True)
        self.assertTrue(serializer.is_valid())

        # Mise à jour de l'événement
        updated_event = serializer.save()

        # Vérification que la mise à jour a bien eu lieu
        self.assertEqual(updated_event.description, 'Updated description.')

