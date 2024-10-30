import uuid

from django.test import TestCase

from BackendTennis.constant import Constant
from BackendTennis.models import NavigationBar, Route, Image, NavigationItem
from BackendTennis.serializers import NavigationBarSerializer


class NavigationBarSerializerTests(TestCase):

    def setUp(self):
        self.image = Image.objects.create(title='NavigationBar Image', type=Constant.IMAGE_TYPE.NAVIGATION_BAR)
        self.image_2 = Image.objects.create(title='NavigationBar Image 2', type=Constant.IMAGE_TYPE.NAVIGATION_BAR)
        self.invalid_image = Image.objects.create(title='Invalid Image', type=Constant.IMAGE_TYPE.PROFESSOR)

        self.logo_route = Route.objects.create(
            name='New Test Route',
            protocol='https',
            domainUrl='test.com'
        )

        self.logo_route_2 = Route.objects.create(
            name='New Test Route 2',
            protocol='http',
            domainUrl='test2.com'
        )

        self.childrenNavigationBars = NavigationItem.objects.create(
            title='NavigationItem'
        )
        self.childrenNavigationBars_2 = NavigationItem.objects.create(
            title='NavigationItem 2'
        )

        self.navigation_item = NavigationItem.objects.create(
            title='New Test NavigationBar'
        )
        self.navigation_item_2 = NavigationItem.objects.create(
            title='New Test NavigationBar 2'
        )

        self.navigation_bar_data = {
            'logo': self.image.id,
            'routeLogo': self.logo_route.id,
            'navigationItems': [self.navigation_item.id]
        }

        self.navigation_bar = NavigationBar.objects.create(
            logo=self.image
        )

    def test_navigation_bar_creation(self):
        serializer = NavigationBarSerializer(data=self.navigation_bar_data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_bar.refresh_from_db()
        self.assertEqual(self.navigation_bar.logo.id, self.image.id, str(serializer.errors))

    def test_navigation_bar_update(self):
        updated_data = {
            'logo': self.image_2.id,
        }
        serializer = NavigationBarSerializer(instance=self.navigation_bar, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_bar.refresh_from_db()
        self.assertEqual(self.navigation_bar.logo.id, self.image_2.id, str(serializer.errors))

    def test_navigation_bar_creation_with_invalid_data(self):
        invalid_data = {'title': 1}
        serializer = NavigationBarSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))

    def test_create_navigation_bar_with_readonly_fields(self):
        data_with_readonly_fields = {
            'id': uuid.uuid4(),
            'createAt': '2024-09-13T10:00:00Z',
            'updateAt': '2024-09-13T10:00:00Z'
        }
        serializer = NavigationBarSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_bar.refresh_from_db()

        self.assertNotEqual(self.navigation_bar.id, data_with_readonly_fields['id'], str(serializer.errors))
        self.assertNotEqual(self.navigation_bar.createAt, data_with_readonly_fields['createAt'],
                            str(serializer.errors))
        self.assertNotEqual(self.navigation_bar.updateAt, data_with_readonly_fields['updateAt'],
                            str(serializer.errors))

    def test_navigation_bar_update_with_partial_data(self):
        updated_data = {
            'routeLogo': self.logo_route_2.id
        }
        serializer = NavigationBarSerializer(instance=self.navigation_bar, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_bar.refresh_from_db()

        self.assertEqual(self.navigation_bar.routeLogo.id, self.logo_route_2.id, str(serializer.errors))

    def test_invalid_type_for_logo(self):
        invalid_data = {
            'logo': self.invalid_image.id
        }
        serializer = NavigationBarSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('logo', serializer.errors)
        self.assertEqual(
            serializer.errors['logo'][0],
            'Image must be of type \'navigation_bar\'.',
            str(serializer.errors)
        )

    def test_invalid_value_for_logo(self):
        invalid_data = {
            'logo': 'no_logo_id'
        }
        serializer = NavigationBarSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('logo', serializer.errors)
        self.assertEqual(
            serializer.errors['logo'][0],
            '“no_logo_id” is not a valid UUID.',
            str(serializer.errors)
        )

    def test_invalid_value_for_routeLogo(self):
        invalid_data = {
            'title': 'Test name',
            'routeLogo': 'no_routeLogo_id'
        }
        serializer = NavigationBarSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('routeLogo', str(serializer.errors))
        self.assertEqual(
            serializer.errors['routeLogo'][0],
            '“no_routeLogo_id” is not a valid UUID.',
            str(serializer.errors))

    def test_invalid_value_for_navigationItems(self):
        invalid_data = {
            'navigationItems': ['no_navigationItem_id']
        }
        serializer = NavigationBarSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), str(serializer.errors))
        self.assertIn('navigationItems', str(serializer.errors))
        self.assertEqual(
            serializer.errors['navigationItems'][0],
            '“no_navigationItem_id” is not a valid UUID.',
            str(serializer.errors))

    def test_update_logo(self):
        data = {
            'logo': self.image_2.id
        }
        serializer = NavigationBarSerializer(instance=self.navigation_bar, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_bar.refresh_from_db()
        self.assertEqual(self.navigation_bar.logo.id, self.image_2.id, str(serializer.errors))

    def test_update_routeLogo(self):
        data = {
            'routeLogo': self.logo_route_2.id
        }
        serializer = NavigationBarSerializer(instance=self.navigation_bar, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_bar.refresh_from_db()
        self.assertEqual(self.navigation_bar.routeLogo.id, self.logo_route_2.id, str(serializer.errors))

    def test_update_navigationItems(self):
        data = {
            'navigationItems': [self.navigation_item.id, self.navigation_item_2.id],
        }
        serializer = NavigationBarSerializer(instance=self.navigation_bar, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        serializer.save()
        self.navigation_bar.refresh_from_db()

        navigation_items_id = self.navigation_bar.navigationItems.values_list('id', flat=True)
        self.assertEqual(self.navigation_bar.navigationItems.count(), 2, str(serializer.errors))
        self.assertIn(self.navigation_item.id, navigation_items_id, str(serializer.errors))
        self.assertIn(self.navigation_item_2.id, navigation_items_id, str(serializer.errors))
