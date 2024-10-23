from rest_framework.test import APITestCase

from BackendTennis.models import Pricing, Image
from BackendTennis.serializers import PricingSerializer


class PricingSerializerTestCase(APITestCase):

    def setUp(self):
        self.image = Image.objects.create(type='sponsor', imageUrl='test_image_url.jpg')
        self.valid_data = {
            'title': 'Test Pricing',
            'license': True,
            'siteAccess': True,
            'extraData': [{'label': 'Test extra data', 'value': 'Test value', 'type': 'string'}],
            'information': 'Test information',
            'price': 100.0,
            'type': 'adult',
            'image': self.image.id
        }

    def test_pricing_serializer_with_valid_data(self):
        serializer = PricingSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['title'], 'Test Pricing')

    def test_pricing_serializer_missing_required_fields(self):
        invalid_data = {
            'description': 'This is a test description',
            # 'title' is missing
            'price': 100.0,
            'type': 'adult',
            'image': self.image.id
        }
        serializer = PricingSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_pricing_serializer_invalid_type(self):
        invalid_data = self.valid_data.copy()
        invalid_data['type'] = 'invalid_type'  # Invalid type
        serializer = PricingSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('type', serializer.errors)
        self.assertIn('Bad Type', serializer.errors['type'][0])

    def test_pricing_serializer_invalid_price(self):
        invalid_data = self.valid_data.copy()
        invalid_data['price'] = -100.0  # Negative price
        serializer = PricingSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_create_pricing(self):
        serializer = PricingSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        pricing = serializer.save()
        self.assertIsInstance(pricing, Pricing)
        self.assertEqual(pricing.title, 'Test Pricing')
        self.assertEqual(pricing.price, 100.0)

    def test_update_pricing(self):
        pricing = Pricing.objects.create(
            title=self.valid_data['title'],
            license=self.valid_data['license'],
            siteAccess=self.valid_data['siteAccess'],
            extraData=self.valid_data['extraData'],
            information=self.valid_data['information'],
            price=self.valid_data['price'],
            type=self.valid_data['type'],
            image=self.image
        )
        update_data = {
            'title': 'Updated Pricing Title',
            'price': 150.0
        }
        serializer = PricingSerializer(pricing, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_pricing = serializer.save()
        self.assertEqual(updated_pricing.title, 'Updated Pricing Title')
        self.assertEqual(updated_pricing.price, 150.0)

    def test_pricing_serializer_with_invalid_image(self):
        invalid_data = self.valid_data.copy()
        invalid_data['image'] = "4ba37213-fe55-47fc-a2e7-0edda285a503"
        serializer = PricingSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('image', serializer.errors)
        self.assertIn('Invalid pk "4ba37213-fe55-47fc-a2e7-0edda285a503"', serializer.errors['image'][0])
