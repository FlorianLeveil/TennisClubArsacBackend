import uuid

from django.test import TestCase

from BackendTennis.constant import Constant
from BackendTennis.models import AboutPage, Image, ClubValue, Sponsor
from BackendTennis.serializers import AboutPageSerializer


class AboutPageSerializerTests(TestCase):

    def setUp(self):
        self.club_image = Image.objects.create(title='Club Image', type=Constant.IMAGE_TYPE.ABOUT_PAGE)
        self.club_image_2 = Image.objects.create(title='Club Image 2', type=Constant.IMAGE_TYPE.ABOUT_PAGE)
        self.invalid_club_image = Image.objects.create(title='Invalid Club Image', type=Constant.IMAGE_TYPE.EVENT)

        self.club_value = ClubValue.objects.create(
            title='ClubValue Title',
            description='ClubValue description',
            order=0
        )
        self.club_value_2 = ClubValue.objects.create(
            title='ClubValue Title 2',
            description='ClubValue description 2',
            order=0
        )

        self.sponsor_image = Image.objects.create(title='Club Image', type=Constant.IMAGE_TYPE.SPONSOR)
        self.sponsor = Sponsor.objects.create(brandName='Sponsor', image=self.sponsor_image)
        self.sponsor_2 = Sponsor.objects.create(brandName='Sponsor 2', image=self.sponsor_image)

        self.about_page_data = {}

    def test_about_page_creation(self):
        serializer = AboutPageSerializer(data=self.about_page_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        about_page = serializer.save()
        self.assertEqual(about_page.clubTitle, None)

    def test_about_page_update(self):
        about_page = AboutPage.objects.create(clubTitle='Old About Page')
        updated_data = {
            'clubTitle': 'Updated About Page',
        }
        serializer = AboutPageSerializer(instance=about_page, data=updated_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_about_page = serializer.save()
        self.assertEqual(updated_about_page.clubTitle, 'Updated About Page')

    def test_about_page_creation_with_invalid_data(self):
        invalid_data = {
            'clubTitle': 'Test About Page' * 50
        }
        serializer = AboutPageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_create_about_page_with_readonly_fields(self):
        data_with_readonly_fields = {
            'id': uuid.uuid4(),
            'createAt': '2024-09-13T10:00:00Z',
            'updateAt': '2024-09-13T10:00:00Z'
        }
        serializer = AboutPageSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        about_page = serializer.save()

        self.assertNotEqual(about_page.id, data_with_readonly_fields['id'])
        self.assertNotEqual(about_page.createAt, data_with_readonly_fields['createAt'])
        self.assertNotEqual(about_page.updateAt, data_with_readonly_fields['updateAt'])

    def test_about_page_update_with_partial_data(self):
        about_page = AboutPage.objects.create(clubTitle='Old About Page')
        updated_data = {
            'clubTitle': 'Partially Updated About Page'
        }
        serializer = AboutPageSerializer(instance=about_page, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_about_page = serializer.save()

        self.assertEqual(updated_about_page.clubTitle, 'Partially Updated About Page')

    def test_invalid_max_length_for_clubTitle(self):
        invalid_data = {
            'clubTitle': 'Test clubTitle Page' * 255
        }
        serializer = AboutPageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('clubTitle', serializer.errors)
        self.assertEqual(serializer.errors['clubTitle'][0], 'Ensure this field has no more than 255 characters.')

    def test_invalid_max_length_for_clubValueTitle(self):
        invalid_data = {
            'clubValueTitle': 'Test clubValueTitle Page' * 255
        }
        serializer = AboutPageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('clubValueTitle', serializer.errors)
        self.assertEqual(serializer.errors['clubValueTitle'][0], 'Ensure this field has no more than 255 characters.')

    def test_invalid_max_length_for_sponsorTitle(self):
        invalid_data = {
            'sponsorTitle': 'Test sponsorTitle Page' * 255
        }
        serializer = AboutPageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('sponsorTitle', serializer.errors)
        self.assertEqual(serializer.errors['sponsorTitle'][0], 'Ensure this field has no more than 255 characters.')

    def test_update_clubTitle(self):
        data = {
            'clubTitle': 'Test clubTitle 2 Page'
        }
        serializer = AboutPageSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        about_page = serializer.save()
        self.assertEqual(about_page.clubTitle, 'Test clubTitle 2 Page')

    def test_update_clubDescription(self):
        data = {
            'clubDescription': 'Test clubDescription 2 Page'
        }
        serializer = AboutPageSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        about_page = serializer.save()
        self.assertEqual(about_page.clubDescription, 'Test clubDescription 2 Page')

    def test_update_clubImage(self):
        data = {
            'clubImage': self.club_image.id
        }
        serializer = AboutPageSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        about_page = serializer.save()

        self.assertEqual(about_page.clubImage.id, self.club_image.id)

        data = {
            'clubImage': self.club_image_2.id
        }
        serializer = AboutPageSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        about_page = serializer.save()

        self.assertEqual(about_page.clubImage.id, self.club_image_2.id)

    def test_update_with_invalid_clubImage(self):
        data = {
            'clubImage': self.invalid_club_image.id
        }
        serializer = AboutPageSerializer(data=data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('clubImage', serializer.errors)
        self.assertEqual(serializer.errors['clubImage'][0], 'Image must be of type \'about_page\'.')

    def test_update_dataCounter(self):
        data = {
            'dataCounter': [
                {
                    'name': 'Adhérents',
                    'count': 180
                },
                {
                    'name': 'Terrains couverts',
                    'count': 2
                },
                {
                    'name': 'Terrains extérieurs',
                    'count': 3
                }

            ]
        }
        serializer = AboutPageSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        about_page = serializer.save()

        self.assertEqual(about_page.dataCounter[0]['name'], 'Adhérents')
        self.assertEqual(about_page.dataCounter[0]['count'], 180)
        self.assertEqual(about_page.dataCounter[1]['name'], 'Terrains couverts')
        self.assertEqual(about_page.dataCounter[1]['count'], 2)
        self.assertEqual(about_page.dataCounter[2]['name'], 'Terrains extérieurs')
        self.assertEqual(about_page.dataCounter[2]['count'], 3)

        data = {
            'dataCounter': [
                {
                    'name': 'Adhérents',
                    'count': 1800
                },
                {
                    'name': 'Terrains couverts',
                    'count': 20
                },
                {
                    'name': 'Terrains extérieurs',
                    'count': 30
                }

            ]
        }
        serializer = AboutPageSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        about_page = serializer.save()

        self.assertEqual(about_page.dataCounter[0]['name'], 'Adhérents')
        self.assertEqual(about_page.dataCounter[0]['count'], 1800)
        self.assertEqual(about_page.dataCounter[1]['name'], 'Terrains couverts')
        self.assertEqual(about_page.dataCounter[1]['count'], 20)
        self.assertEqual(about_page.dataCounter[2]['name'], 'Terrains extérieurs')
        self.assertEqual(about_page.dataCounter[2]['count'], 30)

    def test_update_clubValueTitle(self):
        data = {
            'clubValueTitle': 'Test clubValueTitle 2 Page'
        }
        serializer = AboutPageSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        about_page = serializer.save()
        self.assertEqual(about_page.clubValueTitle, 'Test clubValueTitle 2 Page')

    def test_update_clubValues(self):
        data = {
            'clubValues': [self.club_value.id, self.club_value_2.id]
        }
        serializer = AboutPageSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        about_page = serializer.save()

        self.assertEqual(about_page.clubValues.count(), 2)

    def test_update_sponsorTitle(self):
        data = {
            'sponsorTitle': 'Test sponsorTitle 2 Page'
        }
        serializer = AboutPageSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        about_page = serializer.save()
        self.assertEqual(about_page.sponsorTitle, 'Test sponsorTitle 2 Page')

    def test_update_sponsors(self):
        data = {
            'sponsors': [self.sponsor.id, self.sponsor_2.id]
        }
        serializer = AboutPageSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        about_page = serializer.save()

        self.assertEqual(about_page.sponsors.count(), 2)
