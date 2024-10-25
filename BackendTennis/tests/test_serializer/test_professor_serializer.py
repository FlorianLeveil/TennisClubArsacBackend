import uuid

from django.test import TestCase

from BackendTennis.constant import Constant
from BackendTennis.models import Professor, Image
from BackendTennis.serializers import ProfessorSerializer


class ProfessorSerializerTests(TestCase):

    def setUp(self):
        self.professor_image = Image.objects.create(title='Professor Image', type=Constant.IMAGE_TYPE.PROFESSOR)

        self.invalid_image = Image.objects.create(title='Invalid Image', type='profile')

        self.professor_data = {
            'fullName': 'Test Professor',
            'image': self.professor_image.id,
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6'
        }

    def test_professor_creation(self):
        serializer = ProfessorSerializer(data=self.professor_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        professor = serializer.save()
        self.assertEqual(professor.fullName, 'Test Professor')
        self.assertEqual(professor.image, self.professor_image)

    def test_professor_update(self):
        professor = Professor.objects.create(fullName='Old Professor', image=self.professor_image)
        updated_data = {
            'fullName': 'Updated Professor',
            'image': self.professor_image.id,
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6',
            'order': 2
        }
        serializer = ProfessorSerializer(instance=professor, data=updated_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_professor = serializer.save()
        self.assertEqual(updated_professor.fullName, 'Updated Professor')

    def test_image_type_validation(self):
        invalid_data = {
            'fullName': 'Test Professor',
            'image': self.invalid_image.id,
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6'
        }
        serializer = ProfessorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('Image must be of type \'professor\'.', serializer.errors['image'])

    def test_professor_creation_with_invalid_data(self):
        invalid_data = {
            'fullName': 'Test Professor',
            'image': self.invalid_image.id,
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6'
        }
        serializer = ProfessorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('Image must be of type \'professor\'.', serializer.errors['image'])

    def test_empty_full_name(self):
        invalid_data = {
            'fullName': '',
            'image': self.professor_image.id,
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6'
        }
        serializer = ProfessorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('fullName', serializer.errors)

    def test_create_professor_with_readonly_fields(self):
        data_with_readonly_fields = {
            'fullName': 'Test Professor',
            'image': self.professor_image.id,
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6',
            'id': uuid.uuid4(),
            'createAt': '2024-09-13T10:00:00Z',
            'updateAt': '2024-09-13T10:00:00Z'
        }
        serializer = ProfessorSerializer(data=data_with_readonly_fields)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        professor = serializer.save()

        self.assertNotEqual(professor.id, data_with_readonly_fields['id'])
        self.assertNotEqual(professor.createAt, data_with_readonly_fields['createAt'])
        self.assertNotEqual(professor.updateAt, data_with_readonly_fields['updateAt'])

    def test_professor_update_with_partial_data(self):
        professor = Professor.objects.create(fullName='Old Professor', image=self.professor_image)
        updated_data = {
            'fullName': 'Partially Updated Professor'
        }
        serializer = ProfessorSerializer(instance=professor, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_professor = serializer.save()

        self.assertEqual(updated_professor.fullName, 'Partially Updated Professor')
        self.assertEqual(updated_professor.image, self.professor_image)

    def test_invalid_max_length_for_full_name(self):
        invalid_data = {
            'fullName': 'A' * 255,  # Longueur maximale est 100
            'image': self.professor_image.id,
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6'
        }
        serializer = ProfessorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('fullName', serializer.errors)
        self.assertEqual(serializer.errors['fullName'][0], 'Ensure this field has no more than 250 characters.')

    def test_create_professor_without_image(self):
        invalid_data = {
            'fullName': 'Test Professor'
        }
        serializer = ProfessorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('image', serializer.errors)

    def test_update_professor_invalid_image(self):
        professor = Professor.objects.create(fullName='Valid Professor', image=self.professor_image)
        updated_data = {
            'fullName': 'Still Valid',
            'image': self.invalid_image.id,
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6'
        }
        serializer = ProfessorSerializer(instance=professor, data=updated_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('Image must be of type \'professor\'.', serializer.errors['image'])
