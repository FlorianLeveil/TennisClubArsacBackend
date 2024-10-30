import uuid

from django.test import TestCase

from BackendTennis.models import HomePage, NavigationItem
from BackendTennis.serializers import HomePageSerializer


class HomePageSerializerTests(TestCase):

    def setUp(self):
        self.navigation_item = NavigationItem.objects.create(
            title='New Test NavigationItem',
        )

        self.navigation_item_2 = NavigationItem.objects.create(
            title='New Test NavigationItem 2',
        )

        self.home_page_data = {
            'title': 'New Test HomePage',
        }

        self.home_page = HomePage.objects.create(
            title='New Test HomePage',
        )

    def test_home_page_creation(self):
        serializer = HomePageSerializer(data=self.home_page_data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.home_page.refresh_from_db()
        self.assertEqual(self.home_page.title, 'New Test HomePage', str(serializer.errors))

    def test_home_page_update(self):
        updated_data = {
            'title': 'Updated HomePage',
        }
        serializer = HomePageSerializer(instance=self.home_page, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.home_page.refresh_from_db()
        self.assertEqual(self.home_page.title, 'Updated HomePage', str(serializer.errors))

    def test_home_page_creation_with_invalid_data(self):
        invalid_data = {'title': 'aa'*100}
        serializer = HomePageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))

    def test_create_home_page_with_readonly_fields(self):
        data_with_readonly_fields = {
            'id': uuid.uuid4(),
            'title': 'Test Create ReadonlyFields',
            'createAt': '2024-09-13T10:00:00Z',
            'updateAt': '2024-09-13T10:00:00Z'
        }
        serializer = HomePageSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.home_page.refresh_from_db()

        self.assertNotEqual(self.home_page.id, data_with_readonly_fields['id'], str(serializer.errors))
        self.assertNotEqual(self.home_page.createAt, data_with_readonly_fields['createAt'], str(serializer.errors))
        self.assertNotEqual(self.home_page.updateAt, data_with_readonly_fields['updateAt'], str(serializer.errors))

    def test_home_page_update_with_partial_data(self):
        updated_data = {
            'title': 'Partially Updated HomePage'
        }
        serializer = HomePageSerializer(instance=self.home_page, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.home_page.refresh_from_db()

        self.assertEqual(self.home_page.title, 'Partially Updated HomePage', str(serializer.errors))

    def test_invalid_max_length_for_title(self):
        invalid_data = {
            'title': 'Test name' * 100
        }
        serializer = HomePageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('title', serializer.errors)
        self.assertEqual(
            serializer.errors['title'][0],
            'Ensure this field has no more than 100 characters.',
            str(serializer.errors)
        )

    def test_invalid_value_for_navigationItems(self):
        invalid_data = {
            'title': 'Test name',
            'navigationItems': ['no_navigationItems_id']
        }
        serializer = HomePageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('navigationItems', str(serializer.errors))
        self.assertEqual(
            serializer.errors['navigationItems'][0],
            '“no_navigationItems_id” is not a valid UUID.',
            str(serializer.errors))

    def test_invalid_value_with_valid_value_for_navigationItems(self):
        invalid_data = {
            'title': 'Test name',
            'navigationItems': [self.navigation_item.id, 'no_navigationItems_id']
        }
        serializer = HomePageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('navigationItems', str(serializer.errors))
        self.assertEqual(
            serializer.errors['navigationItems'][0],
            '“no_navigationItems_id” is not a valid UUID.',
            str(serializer.errors))

    def test_update_title(self):
        data = {
            'title': 'Updated Test title'
        }
        serializer = HomePageSerializer(instance=self.home_page, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.home_page.refresh_from_db()
        self.assertEqual(self.home_page.title, 'Updated Test title', str(serializer.errors))

    def test_update_navigationItems(self):
        data = {
            'navigationItems': [self.navigation_item.id, self.navigation_item_2.id],
        }
        serializer = HomePageSerializer(instance=self.home_page, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))

        serializer.save()
        self.home_page.refresh_from_db()

        home_page_rows_id = self.home_page.navigationItems.values_list('id', flat=True)
        self.assertEqual(self.home_page.navigationItems.count(), 2, str(serializer.errors))
        self.assertIn(self.navigation_item.id, home_page_rows_id, str(serializer.errors))
        self.assertIn(self.navigation_item_2.id, home_page_rows_id, str(serializer.errors))
