from django.test import TestCase
from BackendTennis.models import Sponsor, Image
from BackendTennis.serializers import SponsorSerializer
from BackendTennis.constant import Constant
import uuid


class SponsorSerializerTests(TestCase):

    def setUp(self):
        self.sponsor_image = Image.objects.create(title="Sponsor Image", type=Constant.IMAGE_TYPE.SPONSOR)

        self.invalid_image = Image.objects.create(title="Invalid Image", type="profile")

        self.sponsor_data = {
            "brandName": "Test Brand",
            "image": self.sponsor_image.id
        }

    def test_sponsor_creation(self):
        serializer = SponsorSerializer(data=self.sponsor_data)
        self.assertTrue(serializer.is_valid())
        sponsor = serializer.save()
        self.assertEqual(sponsor.brandName, "Test Brand")
        self.assertEqual(sponsor.image, self.sponsor_image)

    def test_sponsor_update(self):
        sponsor = Sponsor.objects.create(brandName="Old Brand", image=self.sponsor_image)
        updated_data = {
            "brandName": "Updated Brand",
            "image": self.sponsor_image.id
        }
        serializer = SponsorSerializer(instance=sponsor, data=updated_data)
        self.assertTrue(serializer.is_valid())
        updated_sponsor = serializer.save()
        self.assertEqual(updated_sponsor.brandName, "Updated Brand")

    def test_image_type_validation(self):
        invalid_data = {
            "brandName": "Test Brand",
            "image": self.invalid_image.id
        }
        serializer = SponsorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Image must be of type 'sponsor'.", serializer.errors['image'])

    def test_sponsor_creation_with_invalid_data(self):
        invalid_data = {
            "brandName": "Test Brand",
            "image": self.invalid_image.id
        }
        serializer = SponsorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Image must be of type 'sponsor'.", serializer.errors['image'])

    def test_empty_brand_name(self):
        invalid_data = {
            "brandName": "",
            "image": self.sponsor_image.id
        }
        serializer = SponsorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('brandName', serializer.errors)

    def test_create_sponsor_with_readonly_fields(self):
        data_with_readonly_fields = {
            "brandName": "Test Brand",
            "image": self.sponsor_image.id,
            "id": uuid.uuid4(),
            "createAt": "2024-09-13T10:00:00Z",
            "updateAt": "2024-09-13T10:00:00Z"
        }
        serializer = SponsorSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid())
        sponsor = serializer.save()

        self.assertNotEqual(sponsor.id, data_with_readonly_fields['id'])
        self.assertNotEqual(sponsor.createAt, data_with_readonly_fields['createAt'])
        self.assertNotEqual(sponsor.updateAt, data_with_readonly_fields['updateAt'])

    def test_sponsor_update_with_partial_data(self):
        sponsor = Sponsor.objects.create(brandName="Old Brand", image=self.sponsor_image)
        updated_data = {
            "brandName": "Partially Updated Brand"
        }
        serializer = SponsorSerializer(instance=sponsor, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_sponsor = serializer.save()

        self.assertEqual(updated_sponsor.brandName, "Partially Updated Brand")
        self.assertEqual(updated_sponsor.image, self.sponsor_image)

    def test_invalid_max_length_for_brand_name(self):
        invalid_data = {
            "brandName": "A" * 101,  # Longueur maximale est 100
            "image": self.sponsor_image.id
        }
        serializer = SponsorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('brandName', serializer.errors)
        self.assertEqual(serializer.errors['brandName'][0], 'Ensure this field has no more than 100 characters.')

    def test_create_sponsor_without_image(self):
        invalid_data = {
            "brandName": "Test Brand"
        }
        serializer = SponsorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('image', serializer.errors)

    def test_update_sponsor_invalid_image(self):
        sponsor = Sponsor.objects.create(brandName="Valid Sponsor", image=self.sponsor_image)
        updated_data = {
            "brandName": "Still Valid",
            "image": self.invalid_image.id
        }
        serializer = SponsorSerializer(instance=sponsor, data=updated_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Image must be of type 'sponsor'.", serializer.errors['image'])
