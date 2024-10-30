import uuid

from django.test import TestCase

from BackendTennis.models import PricingPage, Pricing, Image
from BackendTennis.serializers import PricingPageSerializer


class PricingPageSerializerTests(TestCase):

    def setUp(self):
        self.image = Image.objects.create(type='pricing', imageUrl='test_image_url.jpg')
        self.pricing = Pricing.objects.create(
            title='Test Pricing',
            license=True,
            siteAccess=True,
            extraData=[{'label': 'Test extra data', 'value': 'Test value', 'type': 'string'}],
            information='Test information',
            price=100.0,
            type='adult',
            image=self.image
        )

        self.pricing_2 = Pricing.objects.create(
            title='Test Pricing 2',
            license=True,
            siteAccess=True,
            extraData=[{'label': 'Test extra data', 'value': 'Test value', 'type': 'string'}],
            information='Test information',
            price=100.0,
            type='adult',
            image=self.image
        )

        self.pricing_page_data = {
            'title': 'New Test PricingPage',
        }

        self.pricing_page = PricingPage.objects.create(
            title='New Test PricingPage',
        )

    def test_pricing_page_creation(self):
        serializer = PricingPageSerializer(data=self.pricing_page_data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.pricing_page.refresh_from_db()
        self.assertEqual(self.pricing_page.title, 'New Test PricingPage', str(serializer.errors))

    def test_pricing_page_update(self):
        updated_data = {
            'title': 'Updated PricingPage',
        }
        serializer = PricingPageSerializer(instance=self.pricing_page, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.pricing_page.refresh_from_db()
        self.assertEqual(self.pricing_page.title, 'Updated PricingPage', str(serializer.errors))

    def test_pricing_page_creation_with_invalid_data(self):
        invalid_data = {'title': 'aa' * 255}
        serializer = PricingPageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))

    def test_create_pricing_page_with_readonly_fields(self):
        data_with_readonly_fields = {
            'id': uuid.uuid4(),
            'createAt': '2024-09-13T10:00:00Z',
            'updateAt': '2024-09-13T10:00:00Z'
        }
        serializer = PricingPageSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.pricing_page.refresh_from_db()

        self.assertNotEqual(self.pricing_page.id, data_with_readonly_fields['id'], str(serializer.errors))
        self.assertNotEqual(self.pricing_page.createAt, data_with_readonly_fields['createAt'], str(serializer.errors))
        self.assertNotEqual(self.pricing_page.updateAt, data_with_readonly_fields['updateAt'], str(serializer.errors))

    def test_pricing_page_update_with_partial_data(self):
        updated_data = {
            'title': 'Partially Updated PricingPage'
        }
        serializer = PricingPageSerializer(instance=self.pricing_page, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.pricing_page.refresh_from_db()

        self.assertEqual(self.pricing_page.title, 'Partially Updated PricingPage', str(serializer.errors))

    def test_invalid_max_length_for_title(self):
        invalid_data = {
            'title': 'Test name' * 255
        }
        serializer = PricingPageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('title', serializer.errors)
        self.assertEqual(
            serializer.errors['title'][0],
            'Ensure this field has no more than 255 characters.',
            str(serializer.errors)
        )

    def test_invalid_value_for_pricing(self):
        invalid_data = {
            'title': 'Test name',
            'pricing': ['no_pricing_id']
        }
        serializer = PricingPageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('pricing', str(serializer.errors))
        self.assertEqual(
            serializer.errors['pricing'][0],
            '“no_pricing_id” is not a valid UUID.',
            str(serializer.errors))

    def test_update_title(self):
        data = {
            'title': 'Updated Test title'
        }
        serializer = PricingPageSerializer(instance=self.pricing_page, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.pricing_page.refresh_from_db()
        self.assertEqual(self.pricing_page.title, 'Updated Test title', str(serializer.errors))

    def test_update_description(self):
        data = {
            'description': 'Updated Test description'
        }
        serializer = PricingPageSerializer(instance=self.pricing_page, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.pricing_page.refresh_from_db()
        self.assertEqual(self.pricing_page.description, 'Updated Test description', str(serializer.errors))

    def test_update_pricing(self):
        data = {
            'pricing': [self.pricing.id, self.pricing_2.id],
        }
        serializer = PricingPageSerializer(instance=self.pricing_page, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))

        serializer.save()
        self.pricing_page.refresh_from_db()

        pricing_id = self.pricing_page.pricing.values_list('id', flat=True)
        self.assertEqual(self.pricing_page.pricing.count(), 2, str(serializer.errors))
        self.assertIn(self.pricing.id, pricing_id, str(serializer.errors))
        self.assertIn(self.pricing_2.id, pricing_id, str(serializer.errors))
