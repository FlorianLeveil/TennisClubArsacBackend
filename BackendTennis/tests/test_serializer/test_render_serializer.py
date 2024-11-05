import uuid

from django.test import TestCase

from BackendTennis.models import Render
from BackendTennis.serializers import RenderSerializer


class RenderSerializerTests(TestCase):

    def setUp(self):
        self.render_data = {
            'navBarPosition': 'left',
            'type': 'nav_bar',
            'order': 2
        }

        self.render = Render.objects.create(
            navBarPosition='left',
            type='nav_bar'
        )

    def test_render_creation(self):
        serializer = RenderSerializer(data=self.render_data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.render.refresh_from_db()
        self.assertEqual(self.render.navBarPosition, 'left', str(serializer.errors))

    def test_render_update(self):
        updated_data = {
            'navBarPosition': 'right',
        }
        serializer = RenderSerializer(instance=self.render, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.render.refresh_from_db()
        self.assertEqual(self.render.navBarPosition, 'right', str(serializer.errors))

    def test_render_creation_with_invalid_data(self):
        invalid_data = {}
        serializer = RenderSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))

    def test_create_render_with_readonly_fields(self):
        data_with_readonly_fields = {
            'id': uuid.uuid4(),
            'navBarPosition': 'left',
            'type': 'nav_bar',
            'order': 2,
            'createAt': '2024-09-13T10:00:00Z',
            'updateAt': '2024-09-13T10:00:00Z'
        }
        serializer = RenderSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.render.refresh_from_db()

        self.assertNotEqual(self.render.id, data_with_readonly_fields['id'], str(serializer.errors))
        self.assertNotEqual(self.render.createAt, data_with_readonly_fields['createAt'], str(serializer.errors))
        self.assertNotEqual(self.render.updateAt, data_with_readonly_fields['updateAt'], str(serializer.errors))

    def test_render_update_with_partial_data(self):
        updated_data = {
            'navBarPosition': 'right'
        }
        serializer = RenderSerializer(instance=self.render, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.render.refresh_from_db()

        self.assertEqual(self.render.navBarPosition, 'right', str(serializer.errors))

    def test_invalid_value_for_navBarPosition(self):
        invalid_data = {
            'navBarPosition': 'lefttttt',
            'type': 'nav_bar',
            'order': 2
        }
        serializer = RenderSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('navBarPosition', str(serializer.errors))
        self.assertEqual(
            serializer.errors['navBarPosition'][0],
            '"lefttttt" is not a valid choice.',
            str(serializer.errors))

    def test_invalid_value_for_type(self):
        invalid_data = {
            'navBarPosition': 'left',
            'type': 'baraque',
            'order': 2
        }
        serializer = RenderSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('type', str(serializer.errors))
        self.assertEqual(
            serializer.errors['type'][0],
            '"baraque" is not a valid choice.',
            str(serializer.errors))

    def test_invalid_max_length_for_color(self):
        invalid_data = {
            'navBarPosition': 'left',
            'type': 'nav_bar',
            'order': 2,
            'color': 'red' * 30
        }
        serializer = RenderSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('color', str(serializer.errors))
        self.assertEqual(
            serializer.errors['color'][0],
            'Ensure this field has no more than 30 characters.',
            str(serializer.errors))

    def test_update_order(self):
        data = {
            'order': 23
        }
        serializer = RenderSerializer(instance=self.render, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.render.refresh_from_db()
        self.assertEqual(self.render.order, 23, str(serializer.errors))

    def test_update_navBarPosition(self):
        data = {
            'navBarPosition': 'right'
        }
        serializer = RenderSerializer(instance=self.render, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))

        serializer.save()
        self.render.refresh_from_db()

        self.assertEqual(self.render.navBarPosition, 'right', str(serializer.errors))

    def test_update_visible(self):
        data = {
            'visible': False
        }
        serializer = RenderSerializer(instance=self.render, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))

        serializer.save()
        self.render.refresh_from_db()

        self.assertEqual(self.render.visible, False, str(serializer.errors))

    def test_update_type(self):
        data = {
            'type': 'home_page'
        }
        serializer = RenderSerializer(instance=self.render, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))

        serializer.save()
        self.render.refresh_from_db()

        self.assertEqual(self.render.type, 'home_page', str(serializer.errors))

    def test_update_color(self):
        data = {
            'color': 'cyan'
        }
        serializer = RenderSerializer(instance=self.render, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))

        serializer.save()
        self.render.refresh_from_db()

        self.assertEqual(self.render.color, 'cyan', str(serializer.errors))

    def test_update_isButton(self):
        data = {
            'isButton': True
        }
        serializer = RenderSerializer(instance=self.render, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))

        serializer.save()
        self.render.refresh_from_db()

        self.assertEqual(self.render.isButton, True, str(serializer.errors))
