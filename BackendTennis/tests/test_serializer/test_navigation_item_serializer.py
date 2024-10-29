import uuid

from django.test import TestCase

from BackendTennis.constant import Constant
from BackendTennis.models import NavigationItem, Route, Image, Render, PageRender
from BackendTennis.serializers import NavigationItemSerializer


class NavigationItemSerializerTests(TestCase):

    def setUp(self):
        self.image = Image.objects.create(title='NavigationItem Image', type=Constant.IMAGE_TYPE.NAVIGATION_ITEM)
        self.invalid_image = Image.objects.create(
            title='Invalid NavigationItem Image',
            type=Constant.IMAGE_TYPE.PROFESSOR
        )

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

        self.navBarRender = Render.objects.create(
            navBarPosition='left',
            type='nav_bar'
        )

        self.pageRender = PageRender.objects.create(
            route=self.route,
            render=self.navBarRender
        )

        self.pageRender_2 = PageRender.objects.create(
            route=self.route,
            render=self.navBarRender
        )

        self.childrenNavigationItems = NavigationItem.objects.create(
            title='Child NavigationItem'
        )
        self.childrenNavigationItems_2 = NavigationItem.objects.create(
            title='Child NavigationItem 2'
        )

        self.navigation_item_data = {
            'title': 'New Test NavigationItem'
        }

        self.navigation_item = NavigationItem.objects.create(
            title='New Test NavigationItem'
        )

    def test_navigation_item_creation(self):
        serializer = NavigationItemSerializer(data=self.navigation_item_data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_item.refresh_from_db()
        self.assertEqual(self.navigation_item.title, 'New Test NavigationItem', str(serializer.errors))

    def test_navigation_item_update(self):
        updated_data = {
            'title': 'Updated NavigationItem',
        }
        serializer = NavigationItemSerializer(instance=self.navigation_item, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_item.refresh_from_db()
        self.assertEqual(self.navigation_item.title, 'Updated NavigationItem', str(serializer.errors))

    def test_navigation_item_creation_with_invalid_data(self):
        invalid_data = {}
        serializer = NavigationItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))

    def test_create_navigation_item_with_readonly_fields(self):
        data_with_readonly_fields = {
            'id': uuid.uuid4(),
            'title': 'Test Create ReadonlyFields',
            'createAt': '2024-09-13T10:00:00Z',
            'updateAt': '2024-09-13T10:00:00Z'
        }
        serializer = NavigationItemSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_item.refresh_from_db()

        self.assertNotEqual(self.navigation_item.id, data_with_readonly_fields['id'], str(serializer.errors))
        self.assertNotEqual(self.navigation_item.createAt, data_with_readonly_fields['createAt'],
                            str(serializer.errors))
        self.assertNotEqual(self.navigation_item.updateAt, data_with_readonly_fields['updateAt'],
                            str(serializer.errors))

    def test_navigation_item_update_with_partial_data(self):
        updated_data = {
            'title': 'Partially Updated NavigationItem'
        }
        serializer = NavigationItemSerializer(instance=self.navigation_item, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_item.refresh_from_db()

        self.assertEqual(self.navigation_item.title, 'Partially Updated NavigationItem', str(serializer.errors))

    def test_invalid_max_length_for_title(self):
        invalid_data = {
            'title': 'Test name' * 100
        }
        serializer = NavigationItemSerializer(data=invalid_data)
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
        serializer = NavigationItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('image', serializer.errors)
        self.assertEqual(
            serializer.errors['image'][0],
            'Image must be of type \'navigation_item\'.',
            str(serializer.errors)
        )

    def test_invalid_value_for_image(self):
        invalid_data = {
            'image': 'no_route_id'
        }
        serializer = NavigationItemSerializer(data=invalid_data)
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
        serializer = NavigationItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('route', str(serializer.errors))
        self.assertEqual(
            serializer.errors['route'][0],
            '“no_route_id” is not a valid UUID.',
            str(serializer.errors))

    def test_invalid_value_for_navBarRender(self):
        invalid_data = {
            'title': 'Test name',
            'navBarRender': 'no_navBarRender_id'
        }
        serializer = NavigationItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('navBarRender', str(serializer.errors))
        self.assertEqual(
            serializer.errors['navBarRender'][0],
            '“no_navBarRender_id” is not a valid UUID.',
            str(serializer.errors))

    def test_invalid_value_for_pageRenders(self):
        invalid_data = {
            'title': 'Test name',
            'pageRenders': ['no_pageRenders_id']
        }
        serializer = NavigationItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('pageRenders', str(serializer.errors))
        self.assertEqual(
            serializer.errors['pageRenders'][0],
            '“no_pageRenders_id” is not a valid UUID.',
            str(serializer.errors))

    def test_invalid_value_for_childrenNavigationItems(self):
        invalid_data = {
            'title': 'Test name',
            'childrenNavigationItems': ['no_childrenNavigationItems_id']
        }
        serializer = NavigationItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('childrenNavigationItems', str(serializer.errors))
        self.assertEqual(
            serializer.errors['childrenNavigationItems'][0],
            '“no_childrenNavigationItems_id” is not a valid UUID.',
            str(serializer.errors))

    def test_update_title(self):
        data = {
            'title': 'Updated Test title'
        }
        serializer = NavigationItemSerializer(instance=self.navigation_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_item.refresh_from_db()
        self.assertEqual(self.navigation_item.title, 'Updated Test title', str(serializer.errors))

    def test_update_description(self):
        data = {
            'description': 'Updated Test description'
        }
        serializer = NavigationItemSerializer(instance=self.navigation_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_item.refresh_from_db()
        self.assertEqual(self.navigation_item.description, 'Updated Test description', str(serializer.errors))

    def test_update_image(self):
        data = {
            'image': self.image.id,
        }
        serializer = NavigationItemSerializer(instance=self.navigation_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_item.refresh_from_db()
        self.assertEqual(self.navigation_item.image.id, self.image.id, str(serializer.errors))

    def test_update_route(self):
        data = {
            'route': self.route.id,
        }
        serializer = NavigationItemSerializer(instance=self.navigation_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_item.refresh_from_db()
        self.assertEqual(self.navigation_item.route.id, self.route.id, str(serializer.errors))

    def test_update_navBarRender(self):
        data = {
            'navBarRender': self.navBarRender.id,
        }
        serializer = NavigationItemSerializer(instance=self.navigation_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_item.refresh_from_db()
        self.assertEqual(self.navigation_item.navBarRender.id, self.navBarRender.id, str(serializer.errors))

    def test_update_pageRenders(self):
        data = {
            'pageRenders': [self.pageRender.id, self.pageRender_2.id],
        }
        serializer = NavigationItemSerializer(instance=self.navigation_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_item.refresh_from_db()

        page_renders_id = self.navigation_item.pageRenders.values_list('id', flat=True)
        self.assertEqual(self.navigation_item.pageRenders.count(), 2, str(serializer.errors))
        self.assertIn(self.pageRender.id, page_renders_id, str(serializer.errors))
        self.assertIn(self.pageRender_2.id, page_renders_id, str(serializer.errors))

    def test_update_childrenNavigationItems(self):
        data = {
            'childrenNavigationItems': [self.childrenNavigationItems.id, self.childrenNavigationItems_2.id],
        }
        serializer = NavigationItemSerializer(instance=self.navigation_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_item.refresh_from_db()

        children_navigation_items = self.navigation_item.childrenNavigationItems.values_list('id', flat=True)
        self.assertEqual(self.navigation_item.childrenNavigationItems.count(), 2, str(serializer.errors))
        self.assertIn(self.childrenNavigationItems.id, children_navigation_items, str(serializer.errors))
        self.assertIn(self.childrenNavigationItems_2.id, children_navigation_items, str(serializer.errors))
