from rest_framework.test import APITestCase
from BackendTennis.models import Booking
from BackendTennis.serializers.BookingSerializer import BookingSerializer
from datetime import date


class BookingSerializerTests(APITestCase):

    def setUp(self):
        self.valid_data = {
            'clientFirstName': 'John',
            'clientLastName': 'Doe',
            'clientEmail': 'john.doe@example.com',
            'clientPhoneNumber': '123456789',
            'payed': True,
            'insurance': False,
            'color': 'blue',
            'label': 'Booked',
            'start': '2024-01-01',
            'end': '2024-01-02',
        }

        self.booking = Booking.objects.create(
            clientFirstName='Jane',
            clientLastName='Doe',
            clientEmail='jane.doe@example.com',
            clientPhoneNumber='987654321',
            payed=False,
            insurance=True,
            color='green',
            label='Reserved',
            start=date(2024, 1, 1),
            end=date(2024, 1, 2)
        )

    def test_create_booking_serializer(self):
        """Test creating a new booking with valid data"""
        serializer = BookingSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        booking = serializer.save()
        self.assertEqual(booking.clientFirstName, 'John')
        self.assertEqual(booking.clientLastName, 'Doe')
        self.assertEqual(booking.clientEmail, 'john.doe@example.com')

    def test_create_booking_missing_required_fields(self):
        """Test creating a booking with missing required fields"""
        invalid_data = self.valid_data.copy()
        invalid_data.pop('clientFirstName')  # Remove required field
        serializer = BookingSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('clientFirstName', serializer.errors)

    def test_update_booking_serializer(self):
        """Test updating an existing booking with valid data"""
        update_data = {'clientFirstName': 'Updated John'}
        serializer = BookingSerializer(self.booking, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_booking = serializer.save()
        self.assertEqual(updated_booking.clientFirstName, 'Updated John')

    def test_update_booking_invalid_data(self):
        """Test updating a booking with invalid data"""
        invalid_data = {'clientEmail': 'invalid-email'}  # Invalid email format
        serializer = BookingSerializer(self.booking, data=invalid_data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn('clientEmail', serializer.errors)

    def test_booking_serializer_start_date_after_end_date(self):
        """Test validation error when start date is after end date"""
        invalid_data = self.valid_data.copy()
        invalid_data['start'] = '2024-01-03'  # Start date after end date
        invalid_data['end'] = '2024-01-01'  # End date
        serializer = BookingSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)  # Check for non-field error
        self.assertEqual(serializer.errors['non_field_errors'][0],
                         "Start date must be before or equal to the end date.")

    def test_booking_serializer_missing_optional_fields(self):
        """Test booking creation wSth optional fields missing"""
        valid_data = self.valid_data.copy()
        valid_data.pop('payed')
        valid_data.pop('insurance')
        serializer = BookingSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        booking = serializer.save()
        self.assertEqual(booking.payed, False)  # Default value
        self.assertEqual(booking.insurance, False)  # Default value
