import uuid

from django.test import TestCase

from BackendTennis.models import PageRender, Render, Route
from BackendTennis.serializers import PageRenderSerializer


class PageRenderSerializerTests(TestCase):

    def setUp(self):
        self.render = Render.objects.create(
            navBarPosition='left',
            type='home_page'
        )

        self.render_2 = Render.objects.create(
            navBarPosition='right',
            type='home_page'
        )

        self.route = Route.objects.create(
            name='Test Route',
            protocol='https',
            domainUrl='test.com'
        )

        self.route_2 = Route.objects.create(
            name='Test Route 2',
            protocol='http',
            domainUrl='test2.com'
        )

        self.page_render_data = {
            'route': self.route.id,
            'render': self.render.id
        }

        self.page_render = PageRender.objects.create(
            route=self.route,
            render=self.render
        )

    def test_render_creation(self):
        serializer = PageRenderSerializer(data=self.page_render_data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.page_render.refresh_from_db()
        self.assertEqual(self.page_render.route.id, self.route.id, str(serializer.errors))

    def test_render_update(self):
        updated_data = {
            'route': self.route_2.id,
        }
        serializer = PageRenderSerializer(instance=self.page_render, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.page_render.refresh_from_db()
        self.assertEqual(self.page_render.route.id, self.route_2.id, str(serializer.errors))

    def test_render_creation_with_invalid_data(self):
        invalid_data = {}
        serializer = PageRenderSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))

    def test_create_render_with_readonly_fields(self):
        data_with_readonly_fields = {
            'id': uuid.uuid4(),
            'route': self.route.id,
            'render': self.render.id,
            'createAt': '2024-09-13T10:00:00Z',
            'updateAt': '2024-09-13T10:00:00Z'
        }
        serializer = PageRenderSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.page_render.refresh_from_db()

        self.assertNotEqual(self.page_render.id, data_with_readonly_fields['id'], str(serializer.errors))
        self.assertNotEqual(self.page_render.createAt, data_with_readonly_fields['createAt'], str(serializer.errors))
        self.assertNotEqual(self.page_render.updateAt, data_with_readonly_fields['updateAt'], str(serializer.errors))

    def test_render_update_with_partial_data(self):
        updated_data = {
            'route': self.route_2.id,
        }
        serializer = PageRenderSerializer(instance=self.page_render, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.page_render.refresh_from_db()

        self.assertEqual(self.page_render.route.id, self.route_2.id, str(serializer.errors))

    def test_invalid_render_type(self):
        self.assertEqual(self.page_render.render.id, self.render.id, 'Wrong route id at start test')
        invalid_render = Render.objects.create(
            navBarPosition='right',
            type='nav_bar'
        )
        data = {
            'render': invalid_render.id
        }
        serializer = PageRenderSerializer(instance=self.page_render, data=data, partial=True)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('render', serializer.errors, str(serializer.errors))
        self.assertEqual('Render of PageRender cannot be of \'nav_bar\' type.',
                         serializer.errors['render'][0],
                         str(serializer.errors))

    def test_update_route(self):
        self.assertEqual(self.page_render.route.id, self.route.id, 'Wrong route id at start test')

        data = {
            'route': self.route_2.id
        }
        serializer = PageRenderSerializer(instance=self.page_render, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()

        self.page_render.refresh_from_db()
        self.assertEqual(self.page_render.route.id, self.route_2.id, str(serializer.errors))

    def test_update_render(self):
        self.assertEqual(self.page_render.render.id, self.render.id, 'Wrong route id at start test')

        data = {
            'render': self.render_2.id
        }
        serializer = PageRenderSerializer(instance=self.page_render, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()

        self.page_render.refresh_from_db()
        self.assertEqual(self.page_render.render.id, self.render_2.id, str(serializer.errors))
