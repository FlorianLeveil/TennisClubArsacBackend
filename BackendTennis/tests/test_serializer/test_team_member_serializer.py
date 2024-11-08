import uuid

from django.core.exceptions import ValidationError
from django.test import TestCase

from BackendTennis.constant import Constant
from BackendTennis.models import TeamMember, Image, TeamPage
from BackendTennis.serializers import TeamMemberSerializer, TeamPageSerializer


class TeamMemberSerializerTests(TestCase):

    def setUp(self):
        self.team_member_image = Image.objects.create(title="TeamMember Image", type=Constant.IMAGE_TYPE.TEAM_MEMBER)

        self.invalid_image = Image.objects.create(title="Invalid Image", type="profile")

        self.team_member_data = {
            "fullName": "Test Team Member",
            "image": self.team_member_image.id,
            'role': 'Test User',
            'description': 'test description'
        }

    def test_team_member_creation(self):
        serializer = TeamMemberSerializer(data=self.team_member_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        team_member = serializer.save()
        self.assertEqual(team_member.fullName, "Test Team Member")
        self.assertEqual(team_member.image, self.team_member_image)

    def test_team_member_update(self):
        team_member = TeamMember.objects.create(
            fullName="Old Team Member",
            image=self.team_member_image,
            role='Test User',
            description='test description',
            order=2
        )
        updated_data = {
            "fullName": "Updated Team Member",
            "image": self.team_member_image.id,
            'role': 'Test User',
            'description': 'test description',
            'order': 2
        }
        serializer = TeamMemberSerializer(instance=team_member, data=updated_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_team_member = serializer.save()
        self.assertEqual(updated_team_member.fullName, "Updated Team Member")

    def test_image_type_validation(self):
        invalid_data = {
            "fullName": "Test Team Member",
            "image": self.invalid_image.id,
            'role': 'Test User',
            'description': 'test description'
        }
        serializer = TeamMemberSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn("Image must be of type 'team_member'.", serializer.errors['image'])

    def test_team_member_creation_with_invalid_data(self):
        invalid_data = {
            "fullName": "Test Team Member",
            "image": self.invalid_image.id,
            'role': 'Test User',
            'description': 'test description'
        }
        serializer = TeamMemberSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn("Image must be of type 'team_member'.", serializer.errors['image'])

    def test_empty_full_name(self):
        invalid_data = {
            "fullName": "",
            "image": self.team_member_image.id,
            'role': 'Test User',
            'description': 'test description'
        }
        serializer = TeamMemberSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('fullName', serializer.errors)

    def test_create_team_member_with_readonly_fields(self):
        data_with_readonly_fields = {
            "fullName": "Test Team Member",
            "image": self.team_member_image.id,
            'role': 'Test User',
            'description': 'test description',
            "id": uuid.uuid4(),
            "createAt": "2024-09-13T10:00:00Z",
            "updateAt": "2024-09-13T10:00:00Z"
        }
        serializer = TeamMemberSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        team_member = serializer.save()

        self.assertNotEqual(team_member.id, data_with_readonly_fields['id'])
        self.assertNotEqual(team_member.createAt, data_with_readonly_fields['createAt'])
        self.assertNotEqual(team_member.updateAt, data_with_readonly_fields['updateAt'])

    def test_team_member_update_with_partial_data(self):
        team_member = TeamMember.objects.create(
            fullName="Old Team Member",
            image=self.team_member_image,
            role='Test User',
            description='test description',
            order=2
        )
        updated_data = {
            "fullName": "Partially Updated Team Member"
        }
        serializer = TeamMemberSerializer(instance=team_member, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_team_member = serializer.save()

        self.assertEqual(updated_team_member.fullName, "Partially Updated Team Member")
        self.assertEqual(updated_team_member.image, self.team_member_image)

    def test_invalid_max_length_for_full_name(self):
        invalid_data = {
            "fullName": "A" * 255,  # Longueur maximale est 100
            "image": self.team_member_image.id,
            'role': 'Test User',
            'description': 'test description'
        }
        serializer = TeamMemberSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('fullName', serializer.errors)
        self.assertEqual(serializer.errors['fullName'][0], 'Ensure this field has no more than 250 characters.')

    def test_create_team_member_without_image(self):
        invalid_data = {
            "fullName": "Test Team Member"
        }
        serializer = TeamMemberSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('image', serializer.errors)

    def test_update_team_member_invalid_image(self):
        team_member = TeamMember.objects.create(
            fullName="Old Team Member",
            image=self.team_member_image,
            role='Test User',
            description='test description',
            order=2
        )
        updated_data = {
            "fullName": "Still Valid",
            "image": self.invalid_image.id,
            'role': 'Test User',
            'description': 'test description'
        }
        serializer = TeamMemberSerializer(instance=team_member, data=updated_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn("Image must be of type 'team_member'.", serializer.errors['image'])

    def test_create_full(self):
        full_data = {
            'fullName': 'Test Creation',
            'role': 'Test User',
            'image': self.team_member_image.id,
            'order': 1,
            'description': 'Test Description',
        }
        serializer = TeamMemberSerializer(data=full_data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        team_member = serializer.save()
        team_member.refresh_from_db()

        self.assertEqual(full_data['fullName'], team_member.fullName, str(serializer.errors))
        self.assertEqual(full_data['role'], team_member.role, str(serializer.errors))
        self.assertEqual(full_data['image'], team_member.image.id, str(serializer.errors))
        self.assertEqual(full_data['order'], team_member.order, str(serializer.errors))
        self.assertEqual(full_data['description'], team_member.description, str(serializer.errors))

    def test_update_full(self):
        full_data = {
            'fullName': 'Test Creation',
            'role': 'Test User',
            'image': self.team_member_image.id,
            'order': 1,
            'description': 'Test Description',
        }
        serializer = TeamMemberSerializer(data=full_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        team_member = serializer.save()
        team_member.refresh_from_db()

        update_data = {
            'fullName': 'Updated Creation',
            'role': 'Updated Test User',
            'image': self.team_member_image.id,
            'order': 6,
            'description': 'Updated Description',
        }
        serializer = TeamMemberSerializer(instance=team_member, data=update_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        team_member.refresh_from_db()

        self.assertEqual(update_data['fullName'], team_member.fullName, str(serializer.errors))
        self.assertEqual(update_data['role'], team_member.role, str(serializer.errors))
        self.assertEqual(update_data['image'], team_member.image.id, str(serializer.errors))
        self.assertEqual(update_data['order'], team_member.order, str(serializer.errors))
        self.assertEqual(update_data['description'], team_member.description, str(serializer.errors))

    def test_order_already_used(self):
        data = {
            'fullName': 'First Team Member',
            'image': self.team_member_image.id,
            'order': 2,
            'role': 'Test User',
            'description': 'First Description',
        }

        serializer_first_team_member = TeamMemberSerializer(data=data)
        self.assertTrue(serializer_first_team_member.is_valid(), str(serializer_first_team_member.errors))
        first_team_member = serializer_first_team_member.save()

        team_page = TeamPage.objects.create(teamMembersTitle='Team Page')
        team_page.teamMembers.set([first_team_member])

        data = {
            'fullName': 'New Team Member',
            'image': self.team_member_image.id,
            'order': 2,
            'role': 'Test User',
            'description': 'First Description',
        }

        serializer_new_team_member = TeamMemberSerializer(data=data)
        self.assertTrue(serializer_new_team_member.is_valid(), str(serializer_new_team_member.errors))
        new_team_member = serializer_new_team_member.save()

        serializer_team_page = TeamPageSerializer(
            instance=team_page,
            data={'teamMembers': [first_team_member.id, new_team_member.id]}
        )
        self.assertTrue(serializer_team_page.is_valid(), str(serializer_team_page.errors))

        with self.assertRaises(
                ValidationError,
                msg='Save should failed on Team Member.clean with error : '
                    f'Order [{data['order']}] of TeamMember [{new_team_member.fullName}]'
                    f' already used by another TeamMember in the Team page "{team_page.teamMembersTitle}" .'
        ) as _exception:
            serializer_team_page.save()

        self.assertEqual(
            f'Order [{data['order']}] of TeamMember [{new_team_member.fullName}]'
            f' already used by another TeamMember in the Team page "{team_page.teamMembersTitle}" .',
            _exception.exception.message_dict['order'][0]
        )

    def test_update_order_used_by_other_team_page(self):
        data = {
            'fullName': 'First Team Member',
            'image': self.team_member_image.id,
            'order': 2,
            'role': 'Test User',
            'description': 'First Description',
        }

        serializer_first_team_member = TeamMemberSerializer(data=data)
        self.assertTrue(serializer_first_team_member.is_valid(), str(serializer_first_team_member.errors))
        first_team_member = serializer_first_team_member.save()

        team_page = TeamPage.objects.create(teamMembersTitle='Team Page')
        team_page_2 = TeamPage.objects.create(teamMembersTitle='Team Page 2')

        serializer_team_page = TeamPageSerializer(
            instance=team_page,
            data={'teamMembers': [first_team_member.id]}
        )
        self.assertTrue(serializer_team_page.is_valid(), str(serializer_team_page.errors))
        serializer_team_page.save()

        team_page_team_members = team_page.teamMembers.values_list('id', flat=True)
        self.assertEqual(team_page.teamMembers.count(), 1, str(serializer_team_page.errors))
        self.assertIn(first_team_member.id, team_page_team_members, str(serializer_team_page.errors))

        data = {
            'fullName': 'New Team Member',
            'image': self.team_member_image.id,
            'order': 2,
            'role': 'Test User',
            'description': 'New Description',
        }

        serializer_new_team_member = TeamMemberSerializer(data=data)
        self.assertTrue(serializer_new_team_member.is_valid(), str(serializer_new_team_member.errors))
        new_team_member = serializer_new_team_member.save()

        serializer_team_page_2 = TeamPageSerializer(
            instance=team_page_2,
            data={'teamMembers': [new_team_member.id]}
        )
        self.assertTrue(serializer_team_page_2.is_valid(), str(serializer_team_page_2.errors))
        serializer_team_page_2.save()

        team_page_2.refresh_from_db()

        team_page_2_team_members = team_page_2.teamMembers.values_list('id', flat=True)
        self.assertEqual(team_page_2.teamMembers.count(), 1, str(serializer_team_page_2.errors))
        self.assertIn(new_team_member.id, team_page_2_team_members, str(serializer_team_page_2.errors))

    def test_update_order_used_by_old_team_member(self):
        data = {
            'fullName': 'First Team Member',
            'image': self.team_member_image.id,
            'order': 2,
            'role': 'Test User',
            'description': 'First Description',
        }

        serializer_first_team_member = TeamMemberSerializer(data=data)
        self.assertTrue(serializer_first_team_member.is_valid(), str(serializer_first_team_member.errors))
        first_team_member = serializer_first_team_member.save()

        team_page = TeamPage.objects.create(teamMembersTitle='Team Page')

        serializer_team_page = TeamPageSerializer(
            instance=team_page,
            data={'teamMembers': [first_team_member.id]}
        )
        self.assertTrue(serializer_team_page.is_valid(), str(serializer_team_page.errors))
        serializer_team_page.save()
        team_page.refresh_from_db()

        team_page_team_members = team_page.teamMembers.values_list('id', flat=True)
        self.assertEqual(team_page.teamMembers.count(), 1, str(serializer_team_page.errors))
        self.assertIn(first_team_member.id, team_page_team_members, str(serializer_team_page.errors))

        data = {
            'fullName': 'New Team Member',
            'image': self.team_member_image.id,
            'order': 2,
            'role': 'Test User',
            'description': 'New Description',
        }

        serializer_new_team_member = TeamMemberSerializer(data=data)
        self.assertTrue(serializer_new_team_member.is_valid(), str(serializer_new_team_member.errors))
        new_team_member = serializer_new_team_member.save()

        serializer_team_page = TeamPageSerializer(
            instance=team_page,
            data={'teamMembers': [new_team_member.id]}
        )
        self.assertTrue(serializer_team_page.is_valid(), str(serializer_team_page.errors))
        serializer_team_page.save()
        team_page.refresh_from_db()

        team_page_team_members = team_page.teamMembers.values_list('id', flat=True)
        self.assertEqual(team_page.teamMembers.count(), 1, str(serializer_team_page.errors))
        self.assertIn(new_team_member.id, team_page_team_members, str(serializer_team_page.errors))

    def test_update_order_of_team_member_saved_in_team_page(self):
        data = {
            'fullName': 'First Team Member',
            'image': self.team_member_image.id,
            'order': 2,
            'role': 'Test User',
            'description': 'First Description',
        }

        serializer_first_team_member = TeamMemberSerializer(data=data)
        self.assertTrue(serializer_first_team_member.is_valid(), str(serializer_first_team_member.errors))
        first_team_member = serializer_first_team_member.save()

        team_page = TeamPage.objects.create(teamMembersTitle='Team Page')
        team_page.teamMembers.set([first_team_member])

        data = {
            'fullName': 'New Team Member',
            'image': self.team_member_image.id,
            'order': 3,
            'role': 'Test User',
            'description': 'First Description',
        }

        serializer_new_team_member = TeamMemberSerializer(data=data)
        self.assertTrue(serializer_new_team_member.is_valid(), str(serializer_new_team_member.errors))
        new_team_member = serializer_new_team_member.save()

        serializer_team_page = TeamPageSerializer(
            instance=team_page,
            data={'teamMembers': [first_team_member.id, new_team_member.id]}
        )
        self.assertTrue(serializer_team_page.is_valid(), str(serializer_team_page.errors))
        serializer_team_page.save()
        team_page.refresh_from_db()

        data = {
            'order': 2
        }

        serializer_update_team_member = TeamMemberSerializer(instance=new_team_member, data=data, partial=True)
        self.assertTrue(serializer_update_team_member.is_valid(), str(serializer_update_team_member.errors))

        with self.assertRaises(
                ValidationError,
                msg='Save should failed on Team Member.clean with error : '
                    f'Order [{data['order']}] of TeamMember [{new_team_member.fullName}]'
                    f' already used by another TeamMember in the Team page "{team_page.teamMembersTitle}" .'
        ) as _exception:
            serializer_update_team_member.save()

        self.assertEqual(
            f'Order [{data['order']}] of TeamMember [{new_team_member.fullName}]'
            f' already used by another TeamMember in the Team page "{team_page.teamMembersTitle}" .',
            _exception.exception.message_dict['order'][0]
        )

    def test_order_already_used_at_page_creation(self):
        data = {
            'fullName': 'First Team Member',
            'image': self.team_member_image.id,
            'order': 2,
            'role': 'Test User',
            'description': 'First Description',
        }

        serializer_first_team_member = TeamMemberSerializer(data=data)
        self.assertTrue(serializer_first_team_member.is_valid(), str(serializer_first_team_member.errors))
        first_team_member = serializer_first_team_member.save()

        data = {
            'fullName': 'New Team Member',
            'image': self.team_member_image.id,
            'order': 2,
            'role': 'Test User',
            'description': 'First Description',
        }

        serializer_new_team_member = TeamMemberSerializer(data=data)
        self.assertTrue(serializer_new_team_member.is_valid(), str(serializer_new_team_member.errors))
        new_team_member = serializer_new_team_member.save()

        data_team_page = {'teamMembersTitle': 'Team Page', 'teamMembers': [first_team_member.id, new_team_member.id]}

        serializer_team_page = TeamPageSerializer(
            data=data_team_page
        )
        self.assertTrue(serializer_team_page.is_valid(), str(serializer_team_page.errors))

        with self.assertRaises(
                ValidationError,
                msg='Save should failed on Team Member.clean with error : '
                    f'Order [{data['order']}] of TeamMember [{first_team_member.fullName}]'
                    f' already used by another TeamMember in the Team page "{data_team_page['teamMembersTitle']}" .'
        ) as _exception:
            serializer_team_page.save()

        self.assertEqual(
            f'Order [{data['order']}] of TeamMember [{first_team_member.fullName}]'
            f' already used by another TeamMember in the Team page "{data_team_page['teamMembersTitle']}" .',
            _exception.exception.message_dict['order'][0]
        )
