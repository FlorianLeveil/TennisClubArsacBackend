import uuid

from django.test import TestCase

from BackendTennis.constant import Constant
from BackendTennis.models import TeamMember, Image
from BackendTennis.serializers import TeamMemberSerializer


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
        team_member = TeamMember.objects.create(fullName="Old Team Member", image=self.team_member_image)
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
        team_member = TeamMember.objects.create(fullName="Old Team Member", image=self.team_member_image)
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
        team_member = TeamMember.objects.create(fullName="Valid TeamMember", image=self.team_member_image)
        updated_data = {
            "fullName": "Still Valid",
            "image": self.invalid_image.id,
            'role': 'Test User',
            'description': 'test description'
        }
        serializer = TeamMemberSerializer(instance=team_member, data=updated_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn("Image must be of type 'team_member'.", serializer.errors['image'])
