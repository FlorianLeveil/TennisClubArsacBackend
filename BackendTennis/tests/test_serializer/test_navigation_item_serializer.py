import uuid

from django.core.exceptions import ValidationError
from django.test import TestCase

from BackendTennis.constant import Constant
from BackendTennis.models import NavigationItem, Route, Image, Render, PageRender
from BackendTennis.serializers import NavigationItemSerializer, RenderSerializer


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
        self.child_navBarRender = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=1
        )
        self.child_navBarRender2 = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2
        )
        self.child_navBarRender3 = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=3
        )

        self.navBarRender_2 = Render.objects.create(
            navBarPosition='left',
            type='nav_bar'
        )

        self.invalid_navBarRender_type = Render.objects.create(
            navBarPosition='left',
            type='home_page'
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
            title='New Test NavigationItem',
            navBarRender=self.navBarRender
        )

        self.child_navigation_item = NavigationItem.objects.create(
            title='New Child Test NavigationItem 1',
            navBarRender=self.child_navBarRender
        )

        self.child_navigation_item_2 = NavigationItem.objects.create(
            title='New Child Test NavigationItem 2',
            navBarRender=self.child_navBarRender2
        )

        self.child_navigation_item_3 = NavigationItem.objects.create(
            title='New Child Test NavigationItem 3',
            navBarRender=self.child_navBarRender3
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

    def test_invalid_type_for_navBarRender(self):
        invalid_data = {
            'title': 'Test name',
            'navBarRender': self.invalid_navBarRender_type.id
        }
        serializer = NavigationItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('navBarRender', str(serializer.errors))
        self.assertEqual(
            serializer.errors['navBarRender'][0],
            'navBarRender must be of type \'nav_bar\'.',
            str(serializer.errors))

    def test_root_item_navBarRender_order_already_used(self):
        old_nav_bar_render = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2005
        )

        old_nav_bar_render_2 = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2006
        )

        new_nav_bar_render_with_existing_order = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2005
        )

        data = {
            'title': 'Test name',
            'navBarRender': old_nav_bar_render.id
        }
        serializer_1 = NavigationItemSerializer(data=data)
        self.assertTrue(serializer_1.is_valid(), str(serializer_1.errors))
        serializer_1.save()

        data_2 = {
            'title': 'Test name 2',
            'navBarRender': old_nav_bar_render_2.id
        }
        serializer_2 = NavigationItemSerializer(data=data_2)
        self.assertTrue(serializer_2.is_valid(), str(serializer_2.errors))
        new_element_2 = serializer_2.save()

        serializer_3 = NavigationItemSerializer(
            instance=new_element_2,
            data={'navBarRender': new_nav_bar_render_with_existing_order.id},
            partial=True
        )

        self.assertTrue(serializer_3.is_valid(), str(serializer_3.errors))
        with self.assertRaises(
                ValidationError,
                msg='Save should failed on NavigationItem._validate_order_for_root_items with error : '
                    '\'(root_items) Several elements use the same order [2005] for navBarRender\''
        ):
            serializer_3.save()

    def test_child_items_navBarRender_order_already_used(self):
        new_nav_bar_render = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2020
        )

        new_child_nav_bar_render_1 = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2021
        )
        new_child_nav_bar_render_2 = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2022
        )
        new_child_nav_bar_render_error = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2022
        )
        children_navigation_items = NavigationItem.objects.create(
            title='Child NavigationItem 2',
            navBarRender=new_child_nav_bar_render_1
        )
        children_navigation_items_2 = NavigationItem.objects.create(
            title='Child NavigationItem',
            navBarRender=new_child_nav_bar_render_2
        )

        data = {
            'title': 'Test name',
            'navBarRender': new_nav_bar_render.id,
            'childrenNavigationItems': [children_navigation_items.id, children_navigation_items_2.id]
        }
        serializer = NavigationItemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        children_navigation_items.refresh_from_db()

        serializer = NavigationItemSerializer(
            instance=children_navigation_items,
            data={'navBarRender': new_child_nav_bar_render_error.id},
            partial=True
        )
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        with self.assertRaises(
                ValidationError,
                msg='Save should failed on NavigationItem._validate_order_for_child_items with error : '
                    '\'(child_items) Several elements use the same order [2022] for navBarRender\''
        ):
            serializer.save()

    def test_order_from_childrenNavigationItems_navBarRender_order_already_used(self):
        new_nav_bar_render = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2020
        )

        new_child_nav_bar_render_1 = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2021
        )
        new_child_nav_bar_render_2 = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2022
        )
        new_child_nav_bar_render_error = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2021
        )

        children_navigation_items = NavigationItem.objects.create(
            title='Child NavigationItem',
            navBarRender=new_child_nav_bar_render_1
        )
        children_navigation_items_2 = NavigationItem.objects.create(
            title='Child NavigationItem 2',
            navBarRender=new_child_nav_bar_render_2
        )

        data = {
            'title': 'Test name',
            'navBarRender': new_nav_bar_render.id,
            'childrenNavigationItems': [children_navigation_items.id]
        }
        serializer = NavigationItemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        new_element = serializer.save()
        new_element.refresh_from_db()
        children_navigation_items_3 = NavigationItem.objects.create(
            title='Child NavigationItem 3',
            navBarRender=new_child_nav_bar_render_error
        )

        serializer_2 = NavigationItemSerializer(
            instance=new_element,
            data={
                'childrenNavigationItems': [
                    children_navigation_items.id,
                    children_navigation_items_2.id,
                    children_navigation_items_3.id
                ]
            },
            partial=True
        )

        self.assertTrue(serializer_2.is_valid(), str(serializer_2.errors))

        with self.assertRaises(
                ValidationError,
                msg='Save should failed on NavigationItem._validate_order_for_child_items with error : '
                    '\'(children_navigation_items) Several elements use the same order [2021] for navBarRender\''
        ):
            serializer_2.save()

    def test_navBarRender_update_order_update_already_used_in_parent_brothers(self):
        nav_bar_render = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2005
        )

        nav_bar_render_2 = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2006
        )

        data = {
            'title': 'Test name',
            'navBarRender': nav_bar_render.id
        }
        serializer_1 = NavigationItemSerializer(data=data)
        self.assertTrue(serializer_1.is_valid(), str(serializer_1.errors))
        serializer_1.save()

        data_2 = {
            'title': 'Test name 2',
            'navBarRender': nav_bar_render_2.id
        }
        serializer_2 = NavigationItemSerializer(data=data_2)
        self.assertTrue(serializer_2.is_valid(), str(serializer_2.errors))
        serializer_2.save()

        serializer_render = RenderSerializer(instance=nav_bar_render_2, data={'order': 2005}, partial=True)
        serializer_render.is_valid()

        with self.assertRaises(
                ValidationError,
                msg='Save should failed on NavigationItem._validate_order_for_child_items with error : '
                    '\'(root_items) Several elements use the same order [2005] for navBarRender\''
        ):
            serializer_render.save()

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
        new_nav_bar_render = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2010
        )
        data = {
            'navBarRender': new_nav_bar_render.id,
        }
        serializer = NavigationItemSerializer(instance=self.navigation_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_item.refresh_from_db()
        self.assertEqual(self.navigation_item.navBarRender.id, new_nav_bar_render.id, str(serializer.errors))

    def test_update_navBarRender_with_same_order_in_child(self):
        new_nav_bar_render = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2010
        )

        new_children_nav_bar_render = Render.objects.create(
            navBarPosition='left',
            type='nav_bar',
            order=2010
        )

        navigation_item = NavigationItem.objects.create(
            title='Test NavigationItem'
        )
        children_navigation_items = NavigationItem.objects.create(
            title='Child NavigationItem',
            navBarRender=new_children_nav_bar_render
        )

        data = {
            'navBarRender': new_nav_bar_render.id,
            'childrenNavigationItems': [children_navigation_items.id]
        }
        serializer = NavigationItemSerializer(instance=navigation_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        navigation_item.refresh_from_db()
        self.assertEqual(navigation_item.navBarRender.id, new_nav_bar_render.id, str(serializer.errors))

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
