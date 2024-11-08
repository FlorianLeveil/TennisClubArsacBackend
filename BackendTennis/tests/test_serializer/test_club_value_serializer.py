from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase

from BackendTennis.models import ClubValue, AboutPage
from BackendTennis.serializers import ClubValueSerializer, AboutPageSerializer


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

    def test_create_club_value_full(self):
        data = {
            'title': 'Tennis ClubValue',
            'description': 'Tennis ClubValue description',
            'order': 1
        }

        serializer = ClubValueSerializer(data=data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        club_value = serializer.save()

        self.assertEqual('Tennis ClubValue', club_value.title, str(serializer.errors))
        self.assertEqual('Tennis ClubValue description', club_value.description, str(serializer.errors))
        self.assertEqual(1, club_value.order, str(serializer.errors))

    def test_update_club_value_full(self):
        data = {
            'title': 'Updated ClubValue',
            'description': 'Updated Tennis ClubValue description',
            'order': 20
        }

        serializer = ClubValueSerializer(instance=self.club_value, data=data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        club_value = serializer.save()

        self.assertEqual('Updated ClubValue', club_value.title, str(serializer.errors))
        self.assertEqual('Updated Tennis ClubValue description', club_value.description, str(serializer.errors))
        self.assertEqual(20, club_value.order, str(serializer.errors))

    def test_order_already_used(self):
        data = {
            'title': 'First ClubValue',
            'description': 'First Tennis ClubValue description',
            'order': 10
        }

        serializer_first_club_value = ClubValueSerializer(data=data)
        self.assertTrue(serializer_first_club_value.is_valid(), str(serializer_first_club_value.errors))
        first_club_value = serializer_first_club_value.save()

        about_page = AboutPage.objects.create(clubTitle='About Page')
        about_page.clubValues.set([first_club_value])

        data = {
            'title': 'New ClubValue',
            'description': 'New Tennis ClubValue description',
            'order': 10
        }

        serializer_new_club_value = ClubValueSerializer(data=data)
        self.assertTrue(serializer_new_club_value.is_valid(), str(serializer_new_club_value.errors))
        new_club_value = serializer_new_club_value.save()

        serializer_about_page = AboutPageSerializer(
            instance=about_page,
            data={'clubValues': [first_club_value.id, new_club_value.id]}
        )
        self.assertTrue(serializer_about_page.is_valid(), str(serializer_about_page.errors))

        with self.assertRaises(
                ValidationError,
                msg='Save should failed on ClubValue.clean with error : '
                    f'Order [{data['order']}] of ClubValue [{new_club_value.title}]'
                    f' already used by another ClubValue in the About page "{about_page.clubTitle}" .'
        ) as _exception:
            serializer_about_page.save()

        self.assertEqual(
            f'Order [{data['order']}] of ClubValue [{new_club_value.title}]'
            f' already used by another ClubValue in the About page "{about_page.clubTitle}" .',
            _exception.exception.message_dict['order'][0]
        )

    def test_update_order_used_by_other_about_page(self):
        data = {
            'title': 'First ClubValue',
            'description': 'First Tennis ClubValue description',
            'order': 0
        }

        serializer_first_club_value = ClubValueSerializer(data=data)
        self.assertTrue(serializer_first_club_value.is_valid(), str(serializer_first_club_value.errors))
        first_club_value = serializer_first_club_value.save()

        about_page = AboutPage.objects.create(clubTitle='About Page')
        about_page_2 = AboutPage.objects.create(clubTitle='About Page 2')

        serializer_about_page = AboutPageSerializer(
            instance=about_page,
            data={'clubValues': [first_club_value.id]}
        )
        self.assertTrue(serializer_about_page.is_valid(), str(serializer_about_page.errors))
        serializer_about_page.save()

        about_page_club_values = about_page.clubValues.values_list('id', flat=True)
        self.assertEqual(about_page.clubValues.count(), 1, str(serializer_about_page.errors))
        self.assertIn(first_club_value.id, about_page_club_values, str(serializer_about_page.errors))

        data = {
            'title': 'New ClubValue',
            'description': 'New Tennis ClubValue description',
            'order': 0
        }

        serializer_new_club_value = ClubValueSerializer(data=data)
        self.assertTrue(serializer_new_club_value.is_valid(), str(serializer_new_club_value.errors))
        new_club_value = serializer_new_club_value.save()

        serializer_about_page_2 = AboutPageSerializer(
            instance=about_page_2,
            data={'clubValues': [new_club_value.id]}
        )
        self.assertTrue(serializer_about_page_2.is_valid(), str(serializer_about_page_2.errors))
        serializer_about_page_2.save()

        about_page_2.refresh_from_db()

        about_page_2_club_values = about_page_2.clubValues.values_list('id', flat=True)
        self.assertEqual(about_page_2.clubValues.count(), 1, str(serializer_about_page_2.errors))
        self.assertIn(new_club_value.id, about_page_2_club_values, str(serializer_about_page_2.errors))

    def test_update_order_used_by_old_club_value(self):
        data = {
            'title': 'First ClubValue',
            'description': 'First Tennis ClubValue description',
            'order': 0
        }

        serializer_first_club_value = ClubValueSerializer(data=data)
        self.assertTrue(serializer_first_club_value.is_valid(), str(serializer_first_club_value.errors))
        first_club_value = serializer_first_club_value.save()

        about_page = AboutPage.objects.create(clubTitle='About Page')

        serializer_about_page = AboutPageSerializer(
            instance=about_page,
            data={'clubValues': [first_club_value.id]}
        )
        self.assertTrue(serializer_about_page.is_valid(), str(serializer_about_page.errors))
        serializer_about_page.save()
        about_page.refresh_from_db()

        about_page_club_values = about_page.clubValues.values_list('id', flat=True)
        self.assertEqual(about_page.clubValues.count(), 1, str(serializer_about_page.errors))
        self.assertIn(first_club_value.id, about_page_club_values, str(serializer_about_page.errors))

        data = {
            'title': 'New ClubValue',
            'description': 'New Tennis ClubValue description',
            'order': 0
        }

        serializer_new_club_value = ClubValueSerializer(data=data)
        self.assertTrue(serializer_new_club_value.is_valid(), str(serializer_new_club_value.errors))
        new_club_value = serializer_new_club_value.save()

        serializer_about_page = AboutPageSerializer(
            instance=about_page,
            data={'clubValues': [new_club_value.id]}
        )
        self.assertTrue(serializer_about_page.is_valid(), str(serializer_about_page.errors))
        serializer_about_page.save()
        about_page.refresh_from_db()

        about_page_club_values = about_page.clubValues.values_list('id', flat=True)
        self.assertEqual(about_page.clubValues.count(), 1, str(serializer_about_page.errors))
        self.assertIn(new_club_value.id, about_page_club_values, str(serializer_about_page.errors))

    def test_order_already_used_at_page_creation(self):
        data = {
            'title': 'First ClubValue',
            'description': 'First Tennis ClubValue description',
            'order': 10
        }

        serializer_first_club_value = ClubValueSerializer(data=data)
        self.assertTrue(serializer_first_club_value.is_valid(), str(serializer_first_club_value.errors))
        first_club_value = serializer_first_club_value.save()

        data = {
            'title': 'New ClubValue',
            'description': 'New Tennis ClubValue description',
            'order': 10
        }

        serializer_new_club_value = ClubValueSerializer(data=data)
        self.assertTrue(serializer_new_club_value.is_valid(), str(serializer_new_club_value.errors))
        new_club_value = serializer_new_club_value.save()
        data_about_page = {
            'clubTitle': 'About Page',
            'clubValues': [first_club_value.id, new_club_value.id]
        }

        serializer_about_page = AboutPageSerializer(
            data=data_about_page
        )
        self.assertTrue(serializer_about_page.is_valid(), str(serializer_about_page.errors))

        with self.assertRaises(
                ValidationError,
                msg='Save should failed on ClubValue.clean with error : '
                    f'Order [{data['order']}] of ClubValue [{first_club_value.title}]'
                    f' already used by another ClubValue in the About page "{data_about_page['clubTitle']}" .'
        ) as _exception:
            serializer_about_page.save()

        self.assertEqual(
            f'Order [{data['order']}] of ClubValue [{first_club_value.title}]'
            f' already used by another ClubValue in the About page "{data_about_page['clubTitle']}" .',
            _exception.exception.message_dict['order'][0]
        )
