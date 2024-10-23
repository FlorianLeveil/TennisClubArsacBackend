from datetime import datetime, date

from rest_framework.test import APITestCase

from BackendTennis.models import User, Training
from BackendTennis.serializers import TrainingSerializer


class TrainingSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            birthdate=date(1990, 1, 1)
        )

        self.valid_data = {
            'name': 'Test Training',
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
            'start': datetime(2024, 10, 12),
            'end': datetime(2024, 10, 13),
        }

    def test_training_serializer_with_valid_data(self):
        serializer = TrainingSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], 'Test Training')

    def test_training_serializer_missing_required_fields(self):
        invalid_data = {
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
        }
        serializer = TrainingSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('start', serializer.errors)
        self.assertIn('end', serializer.errors)

    def test_training_serializer_invalid_date(self):
        invalid_data = {
            'name': 'Test Training',
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
            'start': datetime(2024, 10, 15),
            'end': datetime(2024, 10, 13),
        }
        serializer = TrainingSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual('Start date must be before end date.', serializer.errors['non_field_errors'][0])

    def test_create_training(self):
        serializer = TrainingSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        training = serializer.save()
        self.assertIsInstance(training, Training)
        self.assertEqual(training.name, 'Test Training')
        self.assertEqual(training.start.date(), datetime(2024, 10, 12).date())
        self.assertEqual(training.end.date(), datetime(2024, 10, 13).date())

    #
    def test_update_training(self):
        serializer = TrainingSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        training = serializer.save()
        update_data = {
            'name': 'Updated Training Title',
            'start': datetime(2024, 10, 9),
            'end': datetime(2024, 10, 15)
        }
        serializer = TrainingSerializer(training, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_training = serializer.save()
        self.assertEqual(updated_training.name, 'Updated Training Title')
        self.assertEqual(training.start.date(), datetime(2024, 10, 9).date())
        self.assertEqual(training.end.date(), datetime(2024, 10, 15).date())
