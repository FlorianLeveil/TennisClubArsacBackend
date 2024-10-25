import uuid

from django.test import TestCase

from BackendTennis.constant import Constant
from BackendTennis.models import TeamPage, Professor, Image, TeamMember
from BackendTennis.serializers import TeamPageSerializer


class TeamPageSerializerTests(TestCase):

    def setUp(self):
        self.professor_image = Image.objects.create(title='Professor Image', type=Constant.IMAGE_TYPE.PROFESSOR)
        self.professor_1 = Professor.objects.create(fullName='Professor 1', image=self.professor_image)
        self.professor_2 = Professor.objects.create(fullName='Professor 2', image=self.professor_image)
        self.team_members_1 = TeamMember.objects.create(fullName='Team Member 1', image=self.professor_image)
        self.team_members_2 = TeamMember.objects.create(fullName='Team Member 2', image=self.professor_image)
        self.team_page_data = {}

    def test_team_page_creation(self):
        serializer = TeamPageSerializer(data=self.team_page_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        team_page = serializer.save()
        self.assertEqual(team_page.professorsTitle, None)

    def test_team_page_update(self):
        team_page = TeamPage.objects.create(professorsTitle='Old Team Page')
        updated_data = {
            'professorsTitle': 'Updated Team Page',
        }
        serializer = TeamPageSerializer(instance=team_page, data=updated_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_team_page = serializer.save()
        self.assertEqual(updated_team_page.professorsTitle, 'Updated Team Page')

    def test_team_page_creation_with_invalid_data(self):
        invalid_data = {
            'professorsTitle': 'Test Team Page' * 50
        }
        serializer = TeamPageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_create_team_page_with_readonly_fields(self):
        data_with_readonly_fields = {
            'id': uuid.uuid4(),
            'createAt': '2024-09-13T10:00:00Z',
            'updateAt': '2024-09-13T10:00:00Z'
        }
        serializer = TeamPageSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        team_page = serializer.save()

        self.assertNotEqual(team_page.id, data_with_readonly_fields['id'])
        self.assertNotEqual(team_page.createAt, data_with_readonly_fields['createAt'])
        self.assertNotEqual(team_page.updateAt, data_with_readonly_fields['updateAt'])

    def test_team_page_update_with_partial_data(self):
        team_page = TeamPage.objects.create(professorsTitle='Old Team Page')
        updated_data = {
            'professorsTitle': 'Partially Updated Team Page'
        }
        serializer = TeamPageSerializer(instance=team_page, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_team_page = serializer.save()

        self.assertEqual(updated_team_page.professorsTitle, 'Partially Updated Team Page')

    def test_invalid_max_length_for_professorsTitle(self):
        invalid_data = {
            'professorsTitle': 'Test Team Page' * 255
        }
        serializer = TeamPageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('professorsTitle', serializer.errors)
        self.assertEqual(serializer.errors['professorsTitle'][0], 'Ensure this field has no more than 255 characters.')

    def test_invalid_max_length_for_teamMembersTitle(self):
        invalid_data = {
            'teamMembersTitle': 'Test Team Page' * 255
        }
        serializer = TeamPageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('teamMembersTitle', serializer.errors)
        self.assertEqual(serializer.errors['teamMembersTitle'][0], 'Ensure this field has no more than 255 characters.')

    def test_update_professors(self):
        data = {
            'professors': [self.professor_1.id, self.professor_2.id]
        }
        serializer = TeamPageSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        team_page = serializer.save()

        self.assertEqual(team_page.professors.count(), 2)

    def test_update_teamMembers(self):
        data = {
            'teamMembers': [self.team_members_1.id, self.team_members_2.id]
        }
        serializer = TeamPageSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        team_page = serializer.save()

        self.assertEqual(team_page.teamMembers.count(), 2)
