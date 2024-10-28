import uuid

from django.test import TestCase

from BackendTennis.models import Route
from BackendTennis.serializers import RouteSerializer


class RouteSerializerTests(TestCase):

    def setUp(self):
        self.route_data = {
            'name': 'New Test Route',
            'protocol': 'https',
            'domainUrl': 'new_test.com'
        }

        self.route = Route.objects.create(
            name='New Test Route',
            protocol='https',
            domainUrl='test.com'
        )

    def test_route_creation(self):
        serializer = RouteSerializer(data=self.route_data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        route = serializer.save()
        self.assertEqual(route.name, 'New Test Route', str(serializer.errors))

    def test_route_update(self):
        route = Route.objects.create(
            name='Old Route',
            protocol='https',
            domainUrl='test.com'
        )
        updated_data = {
            'name': 'Updated Route',
        }
        serializer = RouteSerializer(instance=route, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        updated_route = serializer.save()
        self.assertEqual(updated_route.name, 'Updated Route', str(serializer.errors))

    def test_route_creation_with_invalid_data(self):
        invalid_data = {}
        serializer = RouteSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))

    def test_create_route_with_readonly_fields(self):
        data_with_readonly_fields = {
            'id': uuid.uuid4(),
            'name': 'New Test Route',
            'protocol': 'https',
            'domainUrl': 'new_test.com',
            'fullUrl': 'je suis une full url',
            'createAt': '2024-09-13T10:00:00Z',
            'updateAt': '2024-09-13T10:00:00Z'
        }
        serializer = RouteSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        route = serializer.save()

        self.assertNotEqual(route.id, data_with_readonly_fields['id'], str(serializer.errors))
        self.assertNotEqual(route.createAt, data_with_readonly_fields['fullUrl'], str(serializer.errors))
        self.assertNotEqual(route.createAt, data_with_readonly_fields['createAt'], str(serializer.errors))
        self.assertNotEqual(route.updateAt, data_with_readonly_fields['updateAt'], str(serializer.errors))

    def test_route_update_with_partial_data(self):
        route = Route.objects.create(
            name='Old Route',
            protocol='https',
            domainUrl='test.com'
        )
        updated_data = {
            'name': 'Partially Updated Route'
        }
        serializer = RouteSerializer(instance=route, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        updated_route = serializer.save()

        self.assertEqual(updated_route.name, 'Partially Updated Route', str(serializer.errors))

    def test_invalid_max_length_for_name(self):
        invalid_data = {
            'name': 'Test name' * 100,
            'protocol': 'https',
            'domainUrl': 'new_test.com'
        }
        serializer = RouteSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('name', serializer.errors)
        self.assertEqual(serializer.errors['name'][0], 'Ensure this field has no more than 100 characters.',
                         str(serializer.errors))

    def test_invalid_value_for_protocol(self):
        invalid_data = {
            'name': 'Test name',
            'protocol': 'NOT HTTP OR HTTPS',
            'domainUrl': 'new_test.com'
        }
        serializer = RouteSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('protocol', str(serializer.errors))
        self.assertEqual(
            serializer.errors['protocol'][0],
            '"NOT HTTP OR HTTPS" is not a valid choice.',
            str(serializer.errors))

    def test_invalid_max_length_for_domainUrl(self):
        invalid_data = {
            'name': 'Test name',
            'protocol': 'https',
            'domainUrl': 'Test domainUrl' * 255
        }
        serializer = RouteSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('domainUrl', str(serializer.errors))
        self.assertEqual(serializer.errors['domainUrl'][0], 'Ensure this field has no more than 255 characters.')

    def test_domainUrl_contain_path(self):
        invalid_data = {
            'name': 'Test name',
            'protocol': 'https',
            'domainUrl': 'test_domainUrl/'
        }
        serializer = RouteSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('domainUrl', str(serializer.errors))
        self.assertEqual(serializer.errors['domainUrl'][0], 'The \'domainUrl\' must not contain a path.')

    def test_invalid_max_length_for_pathUrl(self):
        invalid_data = {
            'name': 'Test name',
            'protocol': 'https',
            'domainUrl': 'test_domainUrl',
            'pathUrl': 'Test pathUrl' * 255
        }
        serializer = RouteSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('pathUrl', str(serializer.errors))
        self.assertEqual(serializer.errors['pathUrl'][0], 'Ensure this field has no more than 255 characters.')

    def test_pathUrl_must_begin_with_slash(self):
        invalid_data = {
            'name': 'Test name',
            'protocol': 'https',
            'domainUrl': 'test_domainUrl',
            'pathUrl': 'Test pathUrl'
        }
        serializer = RouteSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('pathUrl', str(serializer.errors))
        self.assertEqual(serializer.errors['pathUrl'][0], 'The \'pathUrl\' must begin with \'/\'.')

    def test_invalid_max_length_for_componentPath(self):
        invalid_data = {
            'name': 'Test name',
            'protocol': 'https',
            'domainUrl': 'test_domainUrl',
            'componentPath': 'Test componentPath' * 255
        }
        serializer = RouteSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('componentPath', str(serializer.errors))
        self.assertEqual(serializer.errors['componentPath'][0], 'Ensure this field has no more than 255 characters.')

    def test_invalid_max_length_for_metaTitle(self):
        invalid_data = {
            'name': 'Test name',
            'protocol': 'https',
            'domainUrl': 'test_domainUrl',
            'metaTitle': 'Test metaTitle' * 255
        }
        serializer = RouteSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('metaTitle', str(serializer.errors))
        self.assertEqual(serializer.errors['metaTitle'][0], 'Ensure this field has no more than 255 characters.')

    def test_update_name(self):
        data = {
            'name': 'Updated Test name'
        }
        serializer = RouteSerializer(instance=self.route, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        route = serializer.save()
        self.assertEqual(route.name, 'Updated Test name')

    def test_update_protocol(self):
        data = {
            'protocol': 'http',
        }
        serializer = RouteSerializer(instance=self.route, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        route = serializer.save()
        self.assertEqual(route.protocol, 'http', str(serializer.errors))

    def test_update_domainUrl(self):
        data = {
            'domainUrl': 'updated_url.com',
        }
        serializer = RouteSerializer(instance=self.route, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        route = serializer.save()
        self.assertEqual(route.domainUrl, 'updated_url.com', str(serializer.errors))

    def test_update_pathUrl(self):
        data = {
            'pathUrl': '/test',
        }
        serializer = RouteSerializer(instance=self.route, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        route = serializer.save()
        self.assertEqual(route.pathUrl, '/test', str(serializer.errors))

    def test_update_fullUrl(self):
        data = {
            'protocol': 'https',
            'domainUrl': 'new_updated_url.com',
            'pathUrl': '/test',
        }
        serializer = RouteSerializer(instance=self.route, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        route = serializer.save()
        self.assertEqual(
            route.fullUrl,
            f'{data['protocol']}://{data['domainUrl']}{data['pathUrl']}',
            str(serializer.errors)
        )

    def test_update_componentPath(self):
        data = {
            'componentPath': '../views/TestPage.vue',
        }
        serializer = RouteSerializer(instance=self.route, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        route = serializer.save()
        self.assertEqual(route.componentPath, '../views/TestPage.vue', str(serializer.errors))

    def test_update_metaTitle(self):
        data = {
            'metaTitle': 'Test Page | Onglet de Test'
        }
        serializer = RouteSerializer(instance=self.route, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        route = serializer.save()
        self.assertEqual(route.metaTitle, 'Test Page | Onglet de Test', str(serializer.errors))

    def test_update_metaTags(self):
        test_tags = [
            {
                'name': 'description',
                'content':
                    'Ceci est un Test !',
            }
        ],
        data = {
            'metaTags': test_tags
        }
        serializer = RouteSerializer(instance=self.route, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        route = serializer.save()
        self.assertEqual(route.metaTags, test_tags, str(serializer.errors))
