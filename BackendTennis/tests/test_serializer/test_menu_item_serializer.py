import uuid

from django.test import TestCase

from BackendTennis.constant import Constant
from BackendTennis.models import MenuItem, Route, Image, MenuItemRow
from BackendTennis.serializers import MenuItemSerializer


class MenuItemSerializerTests(TestCase):

    def setUp(self):
        self.image = Image.objects.create(title='MenuItem Image', type=Constant.IMAGE_TYPE.MENU_ITEM)
        self.invalid_image = Image.objects.create(title='Invalid MenuItem Image', type=Constant.IMAGE_TYPE.PROFESSOR)

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

        self.menu_item_row = MenuItemRow.objects.create(
            title='New Test MenuItem',
            route=self.route,
            color='green',
            order=1
        )

        self.menu_item_row_2 = MenuItemRow.objects.create(
            title='New Test MenuItemRow 2 ',
            route=self.route_2,
            color='purple',
            order=2
        )

        self.menu_item_data = {
            'title': 'New Test MenuItem',
            'order': 2
        }

        self.menu_item = MenuItem.objects.create(
            title='New Test MenuItem',
            order=1
        )

    def test_menu_item_creation(self):
        serializer = MenuItemSerializer(data=self.menu_item_data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.title, 'New Test MenuItem', str(serializer.errors))

    def test_menu_item_update(self):
        updated_data = {
            'title': 'Updated MenuItem',
        }
        serializer = MenuItemSerializer(instance=self.menu_item, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.title, 'Updated MenuItem', str(serializer.errors))

    def test_menu_item_creation_with_invalid_data(self):
        invalid_data = {}
        serializer = MenuItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))

    def test_create_menu_item_with_readonly_fields(self):
        data_with_readonly_fields = {
            'id': uuid.uuid4(),
            'title': 'Test Create ReadonlyFields',
            'createAt': '2024-09-13T10:00:00Z',
            'updateAt': '2024-09-13T10:00:00Z'
        }
        serializer = MenuItemSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.menu_item.refresh_from_db()

        self.assertNotEqual(self.menu_item.id, data_with_readonly_fields['id'], str(serializer.errors))
        self.assertNotEqual(self.menu_item.createAt, data_with_readonly_fields['createAt'], str(serializer.errors))
        self.assertNotEqual(self.menu_item.updateAt, data_with_readonly_fields['updateAt'], str(serializer.errors))

    def test_menu_item_update_with_partial_data(self):
        updated_data = {
            'title': 'Partially Updated MenuItem'
        }
        serializer = MenuItemSerializer(instance=self.menu_item, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.menu_item.refresh_from_db()

        self.assertEqual(self.menu_item.title, 'Partially Updated MenuItem', str(serializer.errors))

    def test_invalid_max_length_for_title(self):
        invalid_data = {
            'title': 'Test name' * 100
        }
        serializer = MenuItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('title', serializer.errors)
        self.assertEqual(
            serializer.errors['title'][0],
            'Ensure this field has no more than 100 characters.',
            str(serializer.errors)
        )

    def test_invalid_type_for_image(self):
        invalid_data = {
            'image': self.invalid_image.id
        }
        serializer = MenuItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('image', serializer.errors)
        self.assertEqual(
            serializer.errors['image'][0],
            'Image must be of type \'menuitem\'.',
            str(serializer.errors)
        )

    def test_invalid_value_for_image(self):
        invalid_data = {
            'image': 'no_route_id'
        }
        serializer = MenuItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('image', serializer.errors)
        self.assertEqual(
            serializer.errors['image'][0],
            '“no_route_id” is not a valid UUID.',
            str(serializer.errors)
        )

    def test_invalid_value_for_route(self):
        invalid_data = {
            'title': 'Test name',
            'route': 'no_route_id'
        }
        serializer = MenuItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('route', str(serializer.errors))
        self.assertEqual(
            serializer.errors['route'][0],
            '“no_route_id” is not a valid UUID.',
            str(serializer.errors))

    def test_invalid_value_for_rows(self):
        invalid_data = {
            'title': 'Test name',
            'rows': ['no_rows_id']
        }
        serializer = MenuItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('rows', str(serializer.errors))
        self.assertEqual(
            serializer.errors['rows'][0],
            '“no_rows_id” is not a valid UUID.',
            str(serializer.errors))

    def test_invalid_value_with_valid_value_for_rows(self):
        invalid_data = {
            'title': 'Test name',
            'rows': [self.menu_item_row.id, 'no_route_id']
        }
        serializer = MenuItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('rows', str(serializer.errors))
        self.assertEqual(
            serializer.errors['rows'][0],
            '“no_route_id” is not a valid UUID.',
            str(serializer.errors))

    def test_order_already_used(self):
        invalid_data = {
            'title': 'Test name',
            'order': 1
        }
        serializer = MenuItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('order', str(serializer.errors))
        self.assertEqual(
            serializer.errors['order'][0],
            'Another MenuItem already use this order.',
            str(serializer.errors)
        )

    def test_update_title(self):
        data = {
            'title': 'Updated Test title'
        }
        serializer = MenuItemSerializer(instance=self.menu_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.title, 'Updated Test title', str(serializer.errors))

    def test_update_description(self):
        data = {
            'description': 'Updated Test description'
        }
        serializer = MenuItemSerializer(instance=self.menu_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.description, 'Updated Test description', str(serializer.errors))

    def test_update_image(self):
        data = {
            'image': self.image.id,
        }
        serializer = MenuItemSerializer(instance=self.menu_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.image.id, self.image.id, str(serializer.errors))

    def test_update_route(self):
        data = {
            'route': self.route.id,
        }
        serializer = MenuItemSerializer(instance=self.menu_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.route.id, self.route.id, str(serializer.errors))

    def test_update_rows(self):
        data = {
            'rows': [self.menu_item_row.id, self.menu_item_row_2.id],
        }
        serializer = MenuItemSerializer(instance=self.menu_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))

        serializer.save()
        self.menu_item.refresh_from_db()

        menu_item_rows_id = self.menu_item.rows.values_list('id', flat=True)
        self.assertEqual(self.menu_item.rows.count(), 2, str(serializer.errors))
        self.assertIn(self.menu_item_row.id, menu_item_rows_id, str(serializer.errors))
        self.assertIn(self.menu_item_row_2.id, menu_item_rows_id, str(serializer.errors))

    def test_update_order(self):
        data = {
            'order': 12,
        }
        serializer = MenuItemSerializer(instance=self.menu_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.order, 12, str(serializer.errors))
