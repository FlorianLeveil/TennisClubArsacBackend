import uuid

from django.core.exceptions import ValidationError
from django.test import TestCase

from BackendTennis.constant import Constant
from BackendTennis.models import Sponsor, Image, AboutPage
from BackendTennis.serializers import SponsorSerializer, AboutPageSerializer


class SponsorSerializerTests(TestCase):

    def setUp(self):
        self.sponsor_image = Image.objects.create(title='Sponsor Image', type=Constant.IMAGE_TYPE.SPONSOR)

        self.invalid_image = Image.objects.create(title='Invalid Image', type='profile')

        self.sponsor_data = {
            'brandName': 'Test Brand',
            'image': self.sponsor_image.id
        }

    def test_sponsor_creation(self):
        serializer = SponsorSerializer(data=self.sponsor_data)
        self.assertTrue(serializer.is_valid())
        sponsor = serializer.save()
        self.assertEqual(sponsor.brandName, 'Test Brand')
        self.assertEqual(sponsor.image, self.sponsor_image)

    def test_sponsor_update(self):
        sponsor = Sponsor.objects.create(brandName='Old Brand', image=self.sponsor_image)
        updated_data = {
            'brandName': 'Updated Brand',
            'image': self.sponsor_image.id
        }
        serializer = SponsorSerializer(instance=sponsor, data=updated_data)
        self.assertTrue(serializer.is_valid())
        updated_sponsor = serializer.save()
        self.assertEqual(updated_sponsor.brandName, 'Updated Brand')

    def test_image_type_validation(self):
        invalid_data = {
            'brandName': 'Test Brand',
            'image': self.invalid_image.id
        }
        serializer = SponsorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Image must be of type \'sponsor\'.', serializer.errors['image'])

    def test_sponsor_creation_with_invalid_data(self):
        invalid_data = {
            'brandName': 'Test Brand',
            'image': self.invalid_image.id
        }
        serializer = SponsorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Image must be of type \'sponsor\'.', serializer.errors['image'])

    def test_empty_brand_name(self):
        invalid_data = {
            'brandName': "",
            'image': self.sponsor_image.id
        }
        serializer = SponsorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('brandName', serializer.errors)

    def test_create_sponsor_with_readonly_fields(self):
        data_with_readonly_fields = {
            'brandName': 'Test Brand',
            'image': self.sponsor_image.id,
            'id': uuid.uuid4(),
            'createAt': '2024-09-13T10:00:00Z',
            'updateAt': '2024-09-13T10:00:00Z'
        }
        serializer = SponsorSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid())
        sponsor = serializer.save()

        self.assertNotEqual(sponsor.id, data_with_readonly_fields['id'])
        self.assertNotEqual(sponsor.createAt, data_with_readonly_fields['createAt'])
        self.assertNotEqual(sponsor.updateAt, data_with_readonly_fields['updateAt'])

    def test_sponsor_update_with_partial_data(self):
        sponsor = Sponsor.objects.create(brandName='Old Brand', image=self.sponsor_image)
        updated_data = {
            'brandName': 'Partially Updated Brand'
        }
        serializer = SponsorSerializer(instance=sponsor, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_sponsor = serializer.save()

        self.assertEqual(updated_sponsor.brandName, 'Partially Updated Brand')
        self.assertEqual(updated_sponsor.image, self.sponsor_image)

    def test_invalid_max_length_for_brand_name(self):
        invalid_data = {
            'brandName': 'A' * 101,  # Longueur maximale est 100
            'image': self.sponsor_image.id
        }
        serializer = SponsorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('brandName', serializer.errors)
        self.assertEqual(serializer.errors['brandName'][0], 'Ensure this field has no more than 100 characters.')

    def test_create_sponsor_without_image(self):
        invalid_data = {
            'brandName': 'Test Brand'
        }
        serializer = SponsorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('image', serializer.errors)

    def test_update_sponsor_invalid_image(self):
        sponsor = Sponsor.objects.create(brandName='Valid Sponsor', image=self.sponsor_image)
        updated_data = {
            'brandName': 'Still Valid',
            'image': self.invalid_image.id
        }
        serializer = SponsorSerializer(instance=sponsor, data=updated_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Image must be of type \'sponsor\'.', serializer.errors['image'])

    def test_create_sponsor_full(self):
        data = {
            'brandName': 'Test Sponsor',
            'image': self.sponsor_image.id,
            'order': 10
        }

        serializer = SponsorSerializer(data=data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        sponsor = serializer.save()

        self.assertEqual('Test Sponsor', sponsor.brandName, str(serializer.errors))
        self.assertEqual(self.sponsor_image.id, sponsor.image.id, str(serializer.errors))
        self.assertEqual(10, sponsor.order, str(serializer.errors))

    def test_update_sponsor_full(self):
        new_sponsor_image = Image.objects.create(title='New Image', type=Constant.IMAGE_TYPE.SPONSOR)
        sponsor = Sponsor.objects.create(brandName='Test Sponsor', image=self.sponsor_image, order=10)

        data = {
            'brandName': 'Updated Sponsor',
            'image': new_sponsor_image.id,
            'order': 20
        }

        serializer = SponsorSerializer(instance=sponsor, data=data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        new_sponsor = serializer.save()

        self.assertEqual('Updated Sponsor', new_sponsor.brandName, str(serializer.errors))
        self.assertEqual(new_sponsor_image.id, new_sponsor.image.id, str(serializer.errors))
        self.assertEqual(20, new_sponsor.order, str(serializer.errors))

    def test_order_already_used(self):
        data = {
            'brandName': 'First Sponsor',
            'image': self.sponsor_image.id,
            'order': 0
        }

        serializer_first_sponsor = SponsorSerializer(data=data)
        self.assertTrue(serializer_first_sponsor.is_valid(), str(serializer_first_sponsor.errors))
        first_sponsor = serializer_first_sponsor.save()

        about_page = AboutPage.objects.create(clubTitle='About Page')
        about_page.sponsors.set([first_sponsor])

        data = {
            'brandName': 'New Sponsor',
            'image': self.sponsor_image.id,
            'order': 0
        }

        serializer_new_sponsor = SponsorSerializer(data=data)
        self.assertTrue(serializer_new_sponsor.is_valid(), str(serializer_new_sponsor.errors))
        new_sponsor = serializer_new_sponsor.save()

        serializer_about_page = AboutPageSerializer(
            instance=about_page,
            data={'sponsors': [first_sponsor.id, new_sponsor.id]}
        )
        self.assertTrue(serializer_about_page.is_valid(), str(serializer_about_page.errors))

        with self.assertRaises(
                ValidationError,
                msg='Save should failed on Sponsor.clean with error : '
                    f'Order [{data['order']}] of Sponsor [{new_sponsor.brandName}]'
                    f' already used by another Sponsor in the About page "{about_page.clubTitle}" .'
        ) as _exception:
            serializer_about_page.save()

        self.assertEqual(
            f'Order [{data['order']}] of Sponsor [{new_sponsor.brandName}]'
            f' already used by another Sponsor in the About page "{about_page.clubTitle}" .',
            _exception.exception.message_dict['order'][0]
        )

    def test_update_order_used_by_other_about_page(self):
        data = {
            'brandName': 'First Sponsor',
            'image': self.sponsor_image.id,
            'order': 0
        }

        serializer_first_sponsor = SponsorSerializer(data=data)
        self.assertTrue(serializer_first_sponsor.is_valid(), str(serializer_first_sponsor.errors))
        first_sponsor = serializer_first_sponsor.save()

        about_page = AboutPage.objects.create(clubTitle='About Page')
        about_page_2 = AboutPage.objects.create(clubTitle='About Page 2')

        serializer_about_page = AboutPageSerializer(
            instance=about_page,
            data={'sponsors': [first_sponsor.id]}
        )
        self.assertTrue(serializer_about_page.is_valid(), str(serializer_about_page.errors))
        serializer_about_page.save()

        about_page_sponsors = about_page.sponsors.values_list('id', flat=True)
        self.assertEqual(about_page.sponsors.count(), 1, str(serializer_about_page.errors))
        self.assertIn(first_sponsor.id, about_page_sponsors, str(serializer_about_page.errors))

        data = {
            'brandName': 'New Sponsor',
            'image': self.sponsor_image.id,
            'order': 0
        }

        serializer_new_sponsor = SponsorSerializer(data=data)
        self.assertTrue(serializer_new_sponsor.is_valid(), str(serializer_new_sponsor.errors))
        new_sponsor = serializer_new_sponsor.save()

        serializer_about_page_2 = AboutPageSerializer(
            instance=about_page_2,
            data={'sponsors': [new_sponsor.id]}
        )
        self.assertTrue(serializer_about_page_2.is_valid(), str(serializer_about_page_2.errors))
        serializer_about_page_2.save()

        about_page_2.refresh_from_db()

        about_page_2_sponsors = about_page_2.sponsors.values_list('id', flat=True)
        self.assertEqual(about_page_2.sponsors.count(), 1, str(serializer_about_page_2.errors))
        self.assertIn(new_sponsor.id, about_page_2_sponsors, str(serializer_about_page_2.errors))

    def test_update_order_used_by_old_sponsor(self):
        data = {
            'brandName': 'First Sponsor',
            'image': self.sponsor_image.id,
            'order': 0
        }

        serializer_first_sponsor = SponsorSerializer(data=data)
        self.assertTrue(serializer_first_sponsor.is_valid(), str(serializer_first_sponsor.errors))
        first_sponsor = serializer_first_sponsor.save()

        about_page = AboutPage.objects.create(clubTitle='About Page')

        serializer_about_page = AboutPageSerializer(
            instance=about_page,
            data={'sponsors': [first_sponsor.id]}
        )
        self.assertTrue(serializer_about_page.is_valid(), str(serializer_about_page.errors))
        serializer_about_page.save()
        about_page.refresh_from_db()

        about_page_sponsors = about_page.sponsors.values_list('id', flat=True)
        self.assertEqual(about_page.sponsors.count(), 1, str(serializer_about_page.errors))
        self.assertIn(first_sponsor.id, about_page_sponsors, str(serializer_about_page.errors))

        data = {
            'brandName': 'New Sponsor',
            'image': self.sponsor_image.id,
            'order': 0
        }

        serializer_new_sponsor = SponsorSerializer(data=data)
        self.assertTrue(serializer_new_sponsor.is_valid(), str(serializer_new_sponsor.errors))
        new_sponsor = serializer_new_sponsor.save()

        serializer_about_page = AboutPageSerializer(
            instance=about_page,
            data={'sponsors': [new_sponsor.id]}
        )
        self.assertTrue(serializer_about_page.is_valid(), str(serializer_about_page.errors))
        serializer_about_page.save()
        about_page.refresh_from_db()

        about_page_sponsors = about_page.sponsors.values_list('id', flat=True)
        self.assertEqual(about_page.sponsors.count(), 1, str(serializer_about_page.errors))
        self.assertIn(new_sponsor.id, about_page_sponsors, str(serializer_about_page.errors))

    def test_order_already_used_at_page_creation(self):
        data = {
            'brandName': 'First Sponsor',
            'image': self.sponsor_image.id,
            'order': 0
        }

        serializer_first_sponsor = SponsorSerializer(data=data)
        self.assertTrue(serializer_first_sponsor.is_valid(), str(serializer_first_sponsor.errors))
        first_sponsor = serializer_first_sponsor.save()

        data = {
            'brandName': 'New Sponsor',
            'image': self.sponsor_image.id,
            'order': 0
        }

        serializer_new_sponsor = SponsorSerializer(data=data)
        self.assertTrue(serializer_new_sponsor.is_valid(), str(serializer_new_sponsor.errors))
        new_sponsor = serializer_new_sponsor.save()

        data_about_page = {
            'clubTitle': 'About Page',
            'sponsors': [first_sponsor.id, new_sponsor.id]
        }

        serializer_about_page = AboutPageSerializer(
            data=data_about_page
        )
        self.assertTrue(serializer_about_page.is_valid(), str(serializer_about_page.errors))

        with self.assertRaises(
                ValidationError,
                msg='Save should failed on Sponsor.clean with error : '
                    f'Order [{data['order']}] of Sponsor [{first_sponsor.brandName}]'
                    f' already used by another Sponsor in the About page "{data_about_page['clubTitle']}" .'
        ) as _exception:
            serializer_about_page.save()

        self.assertEqual(
            f'Order [{data['order']}] of Sponsor [{first_sponsor.brandName}]'
            f' already used by another Sponsor in the About page "{data_about_page['clubTitle']}" .',
            _exception.exception.message_dict['order'][0]
        )
