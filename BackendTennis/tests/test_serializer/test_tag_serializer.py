from rest_framework.test import APITestCase
from BackendTennis.models import Tag
from BackendTennis.serializers import TagSerializer


class TagSerializerTests(APITestCase):

    def test_create_tag_with_only_text(self):
        data = {'name': 'eXample Tag'}
        serializer = TagSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        tag = serializer.save()

        self.assertEqual(tag.name, 'Example tag')

    def test_create_tag_with_digit_and_text(self):
        data = {'name': '2024 upcoming Event'}
        serializer = TagSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        tag = serializer.save()

        self.assertEqual(tag.name, '2024 Upcoming event')

    def test_create_tag_with_only_digits(self):
        data = {'name': '2024'}
        serializer = TagSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        tag = serializer.save()

        self.assertEqual(tag.name, '2024')

    def test_create_tag_with_multiple_spaces(self):
        data = {'name': 'Example   Tag   With  Spaces'}
        serializer = TagSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        tag = serializer.save()

        self.assertEqual(tag.name, 'Example tag with spaces')

    def test_tag_uniqueness_on_create(self):
        Tag.objects.create(name='Unique tag')

        data = {'name': 'Unique Tag'}
        serializer = TagSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'][0], "Tag with this name already exists.")

    def test_tag_uniqueness_on_update(self):
        tag1 = Tag.objects.create(name='Tag 1')
        tag2 = Tag.objects.create(name='Tag 2')

        serializer = TagSerializer(tag2, data={'name': 'Tag 1'}, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'][0], "Tag with this name already exists.")

    def test_tag_uniqueness_on_update_two(self):
        tag1 = Tag.objects.create(name='Tag test')
        tag2 = Tag.objects.create(name='Tag test2')

        serializer = TagSerializer(tag2, data={'name': 'Tag Test'}, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'][0], "Tag with this name already exists.")

    def test_update_tag_format(self):
        tag = Tag.objects.create(name='Initial Tag')

        data = {'name': 'new   Tag  Name'}
        serializer = TagSerializer(tag, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_tag = serializer.save()

        self.assertEqual(updated_tag.name, 'New tag name')

    def test_update_tag_with_digits_and_text(self):
        tag = Tag.objects.create(name='Old Tag')

        data = {'name': '2025   future   Event'}
        serializer = TagSerializer(tag, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_tag = serializer.save()

        self.assertEqual(updated_tag.name, '2025 Future event')
