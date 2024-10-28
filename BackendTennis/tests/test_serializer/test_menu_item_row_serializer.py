import uuid

from django.test import TestCase

from BackendTennis.models import MenuItemRow, Route
from BackendTennis.serializers import MenuItemRowSerializer


class MenuItemRowSerializerTests(TestCase):

    def setUp(self):
        self.route = Route.objects.create(
            name='New Test Route',
            protocol='https',
            domainUrl='test.com'
        )

        self.route_2 = Route.objects.create(
            name='New Test Route 2',
            protocol='http',
            domainUrl='test2.com'
        )

        self.menu_item_row_data = {
            'title': 'New Test MenuItemRow',
            'route': self.route.id,
            'color': 'red',
            'order': 2
        }

        self.menu_item_row = MenuItemRow.objects.create(
            title='New Test MenuItemRow',
            route=self.route,
            color='green',
            order=1
        )

    def test_menu_item_row_creation(self):
        serializer = MenuItemRowSerializer(data=self.menu_item_row_data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        menu_item_row = serializer.save()
        self.assertEqual(menu_item_row.title, 'New Test MenuItemRow', str(serializer.errors))

    def test_menu_item_row_update(self):
        updated_data = {
            'title': 'Updated MenuItemRow',
        }
        serializer = MenuItemRowSerializer(instance=self.menu_item_row, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        updated_menu_item_row = serializer.save()
        self.assertEqual(updated_menu_item_row.title, 'Updated MenuItemRow', str(serializer.errors))

    def test_menu_item_row_creation_with_invalid_data(self):
        invalid_data = {}
        serializer = MenuItemRowSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))

    def test_create_menu_item_row_with_readonly_fields(self):
        data_with_readonly_fields = {
            'id': uuid.uuid4(),
            'title': 'Test Create ReadonlyFields',
            'createAt': '2024-09-13T10:00:00Z',
            'updateAt': '2024-09-13T10:00:00Z'
        }
        serializer = MenuItemRowSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        menu_item_row = serializer.save()

        self.assertNotEqual(menu_item_row.id, data_with_readonly_fields['id'], str(serializer.errors))
        self.assertNotEqual(menu_item_row.createAt, data_with_readonly_fields['createAt'], str(serializer.errors))
        self.assertNotEqual(menu_item_row.updateAt, data_with_readonly_fields['updateAt'], str(serializer.errors))

    def test_menu_item_row_update_with_partial_data(self):
        updated_data = {
            'title': 'Partially Updated MenuItemRow'
        }
        serializer = MenuItemRowSerializer(instance=self.menu_item_row, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        updated_menu_item_row = serializer.save()

        self.assertEqual(updated_menu_item_row.title, 'Partially Updated MenuItemRow', str(serializer.errors))

    def test_invalid_max_length_for_title(self):
        invalid_data = {
            'title': 'Test name' * 100
        }
        serializer = MenuItemRowSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('title', serializer.errors)
        self.assertEqual(
            serializer.errors['title'][0],
            'Ensure this field has no more than 100 characters.',
            str(serializer.errors)
        )

    def test_invalid_value_for_route(self):
        invalid_data = {
            'title': 'Test name',
            'route': 'no_route_id'
        }
        serializer = MenuItemRowSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('route', str(serializer.errors))
        self.assertEqual(
            serializer.errors['route'][0],
            '“no_route_id” is not a valid UUID.',
            str(serializer.errors))

    def test_invalid_max_length_for_color(self):
        invalid_data = {
            'title': 'Test name',
            'color': 'green' * 100
        }
        serializer = MenuItemRowSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('color', str(serializer.errors))
        self.assertEqual(
            serializer.errors['color'][0],
            'Ensure this field has no more than 100 characters.',
            str(serializer.errors)
        )

    def test_order_already_used(self):
        invalid_data = {
            'title': 'Test name',
            'order': 1
        }
        serializer = MenuItemRowSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('order', str(serializer.errors))
        self.assertEqual(
            serializer.errors['order'][0],
            'Another MenuItemRow already use this order.',
            str(serializer.errors)
        )

    def test_update_title(self):
        data = {
            'title': 'Updated Test title'
        }
        serializer = MenuItemRowSerializer(instance=self.menu_item_row, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        menu_item_row = serializer.save()
        self.assertEqual(menu_item_row.title, 'Updated Test title', str(serializer.errors))

    def test_update_route(self):
        data = {
            'route': self.route_2.id,
        }
        serializer = MenuItemRowSerializer(instance=self.menu_item_row, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        menu_item_row = serializer.save()
        self.assertEqual(menu_item_row.route.id, self.route_2.id, str(serializer.errors))

    def test_update_color(self):
        data = {
            'color': 'pink',
        }
        serializer = MenuItemRowSerializer(instance=self.menu_item_row, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        menu_item_row = serializer.save()
        self.assertEqual(menu_item_row.color, 'pink', str(serializer.errors))

    def test_update_order(self):
        data = {
            'order': 12,
        }
        serializer = MenuItemRowSerializer(instance=self.menu_item_row, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        menu_item_row = serializer.save()
        self.assertEqual(menu_item_row.order, 12, str(serializer.errors))
