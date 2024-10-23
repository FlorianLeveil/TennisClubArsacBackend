from datetime import datetime, date

from rest_framework.test import APITestCase

from BackendTennis.models import User, Tournament
from BackendTennis.serializers import TournamentSerializer


class TournamentSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            birthdate=date(1990, 1, 1)
        )

        self.valid_data = {
            'name': 'Test Tournament',
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
            'start': datetime(2024, 10, 12),
            'end': datetime(2024, 10, 13),
        }

    def test_tournament_serializer_with_valid_data(self):
        serializer = TournamentSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], 'Test Tournament')

    def test_tournament_serializer_missing_required_fields(self):
        invalid_data = {
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
        }
        serializer = TournamentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('start', serializer.errors)
        self.assertIn('end', serializer.errors)

    def test_tournament_serializer_invalid_date(self):
        invalid_data = {
            'name': 'Test Tournament',
            'participants': [self.user.id],
            'unregisteredParticipants': [],
            'cancel': False,
            'start': datetime(2024, 10, 15),
            'end': datetime(2024, 10, 13),
        }
        serializer = TournamentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual('Start date must be before end date.', serializer.errors['non_field_errors'][0])

    def test_create_tournament(self):
        serializer = TournamentSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        tournament = serializer.save()
        self.assertIsInstance(tournament, Tournament)
        self.assertEqual(tournament.name, 'Test Tournament')
        self.assertEqual(tournament.start.date(), datetime(2024, 10, 12).date())
        self.assertEqual(tournament.end.date(), datetime(2024, 10, 13).date())

    #
    def test_update_tournament(self):
        serializer = TournamentSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        tournament = serializer.save()
        update_data = {
            'name': 'Updated Tournament Title',
            'start': datetime(2024, 10, 9),
            'end': datetime(2024, 10, 15)
        }
        serializer = TournamentSerializer(tournament, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_tournament = serializer.save()
        self.assertEqual(updated_tournament.name, 'Updated Tournament Title')
        self.assertEqual(tournament.start.date(), datetime(2024, 10, 9).date())
        self.assertEqual(tournament.end.date(), datetime(2024, 10, 15).date())
