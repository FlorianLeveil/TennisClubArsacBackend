import uuid

from django.core.exceptions import ValidationError
from django.test import TestCase

from BackendTennis.constant import Constant
from BackendTennis.models import Professor, Image, TeamPage
from BackendTennis.serializers import ProfessorSerializer, TeamPageSerializer


class ProfessorSerializerTests(TestCase):

    def setUp(self):
        self.professor_image = Image.objects.create(title='Professor Image', type=Constant.IMAGE_TYPE.PROFESSOR)

        self.invalid_image = Image.objects.create(title='Invalid Image', type='profile')

        self.professor_data = {
            'fullName': 'Test Professor',
            'image': self.professor_image.id,
            'year_experience': '6 ans',
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
        professor = Professor.objects.create(
            fullName='Old Professor',
            image=self.professor_image,
            role='Test User',
            year_experience='567 ans',
            diploma='E',
            best_rank='6',
            order=6
        )
        updated_data = {
            'fullName': 'Updated Professor',
            'image': self.professor_image.id,
            'role': 'Test User',
            'year_experience': '6',
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
            'year_experience': 6,
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
            'year_experience': 6,
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
            'year_experience': 6,
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
            'year_experience': '6 ans',
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
        professor = Professor.objects.create(
            fullName='Old Professor',
            image=self.professor_image,
            role='Test User',
            year_experience='567 ans',
            diploma='E',
            best_rank='6',
            order=6
        )
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
            'year_experience': 6,
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
        professor = Professor.objects.create(
            fullName='Old Professor',
            image=self.professor_image,
            role='Test User',
            year_experience='567 ans',
            diploma='E',
            best_rank='6',
            order=6
        )
        updated_data = {
            'fullName': 'Still Valid',
            'image': self.invalid_image.id,
            'year_experience': 6,
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6'
        }
        serializer = ProfessorSerializer(instance=professor, data=updated_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('Image must be of type \'professor\'.', serializer.errors['image'])

    def test_create_full(self):
        full_data = {
            'fullName': 'Test Creation',
            'role': 'Test User',
            'image': self.professor_image.id,
            'order': 1,
            'diploma': 'BE',
            'year_experience': '3 ans',
            'best_rank': '1/6',
        }
        serializer = ProfessorSerializer(data=full_data)
        self.assertTrue(serializer.is_valid(), str(serializer.errors))
        professor = serializer.save()
        professor.refresh_from_db()

        self.assertEqual(full_data['fullName'], professor.fullName, str(serializer.errors))
        self.assertEqual(full_data['role'], professor.role, str(serializer.errors))
        self.assertEqual(full_data['image'], professor.image.id, str(serializer.errors))
        self.assertEqual(full_data['order'], professor.order, str(serializer.errors))
        self.assertEqual(full_data['diploma'], professor.diploma, str(serializer.errors))
        self.assertEqual(full_data['year_experience'], professor.year_experience, str(serializer.errors))
        self.assertEqual(full_data['best_rank'], professor.best_rank, str(serializer.errors))

    def test_update_full(self):
        full_data = {
            'fullName': 'Test Creation',
            'role': 'Test User',
            'image': self.professor_image.id,
            'order': 1,
            'diploma': 'BE',
            'year_experience': '3 ans',
            'best_rank': '1/6',
        }
        serializer = ProfessorSerializer(data=full_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        professor = serializer.save()
        professor.refresh_from_db()

        update_data = {
            'fullName': 'Updated Creation',
            'role': 'Updated Test User',
            'image': self.professor_image.id,
            'order': 6,
            'diploma': 'DE',
            'year_experience': '78 ans',
            'best_rank': '0',
        }
        serializer = ProfessorSerializer(instance=professor, data=update_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        professor.refresh_from_db()

        self.assertEqual(update_data['fullName'], professor.fullName, str(serializer.errors))
        self.assertEqual(update_data['role'], professor.role, str(serializer.errors))
        self.assertEqual(update_data['image'], professor.image.id, str(serializer.errors))
        self.assertEqual(update_data['order'], professor.order, str(serializer.errors))
        self.assertEqual(update_data['diploma'], professor.diploma, str(serializer.errors))
        self.assertEqual(update_data['year_experience'], professor.year_experience, str(serializer.errors))
        self.assertEqual(update_data['best_rank'], professor.best_rank, str(serializer.errors))

    def test_order_already_used(self):
        data = {
            'fullName': 'First Professor',
            'image': self.professor_image.id,
            'year_experience': '6 ans',
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6',
            'order': 67
        }

        serializer_first_professor = ProfessorSerializer(data=data)
        self.assertTrue(serializer_first_professor.is_valid(), str(serializer_first_professor.errors))
        first_professor = serializer_first_professor.save()

        team_page = TeamPage.objects.create(professorsTitle='Team Page')
        team_page.professors.set([first_professor])

        data = {
            'fullName': 'New Professor',
            'image': self.professor_image.id,
            'year_experience': '6 ans',
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6',
            'order': 67
        }

        serializer_new_professor = ProfessorSerializer(data=data)
        self.assertTrue(serializer_new_professor.is_valid(), str(serializer_new_professor.errors))
        new_professor = serializer_new_professor.save()

        serializer_team_page = TeamPageSerializer(
            instance=team_page,
            data={'professors': [first_professor.id, new_professor.id]}
        )
        self.assertTrue(serializer_team_page.is_valid(), str(serializer_team_page.errors))

        with self.assertRaises(
                ValidationError,
                msg='Save should failed on Professor.clean with error : '
                    f'Order [{data['order']}] of Professor [{new_professor.fullName}]'
                    f' already used by another Professor in the Team page "{team_page.professorsTitle}" .'
        ) as _exception:
            serializer_team_page.save()

        self.assertEqual(
            f'Order [{data['order']}] of Professor [{new_professor.fullName}]'
            f' already used by another Professor in the Team page "{team_page.professorsTitle}" .',
            _exception.exception.message_dict['order'][0]
        )

    def test_update_order_used_by_other_team_page(self):
        data = {
            'fullName': 'First Professor',
            'image': self.professor_image.id,
            'year_experience': '6 ans',
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6'
        }

        serializer_first_professor = ProfessorSerializer(data=data)
        self.assertTrue(serializer_first_professor.is_valid(), str(serializer_first_professor.errors))
        first_professor = serializer_first_professor.save()

        team_page = TeamPage.objects.create(professorsTitle='Team Page')
        team_page_2 = TeamPage.objects.create(professorsTitle='Team Page 2')

        serializer_team_page = TeamPageSerializer(
            instance=team_page,
            data={'professors': [first_professor.id]}
        )
        self.assertTrue(serializer_team_page.is_valid(), str(serializer_team_page.errors))
        serializer_team_page.save()

        team_page_professors = team_page.professors.values_list('id', flat=True)
        self.assertEqual(team_page.professors.count(), 1, str(serializer_team_page.errors))
        self.assertIn(first_professor.id, team_page_professors, str(serializer_team_page.errors))

        data = {
            'fullName': 'New Professor',
            'image': self.professor_image.id,
            'year_experience': '6 ans',
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6'
        }

        serializer_new_professor = ProfessorSerializer(data=data)
        self.assertTrue(serializer_new_professor.is_valid(), str(serializer_new_professor.errors))
        new_professor = serializer_new_professor.save()

        serializer_team_page_2 = TeamPageSerializer(
            instance=team_page_2,
            data={'professors': [new_professor.id]}
        )
        self.assertTrue(serializer_team_page_2.is_valid(), str(serializer_team_page_2.errors))
        serializer_team_page_2.save()

        team_page_2.refresh_from_db()

        team_page_2_professors = team_page_2.professors.values_list('id', flat=True)
        self.assertEqual(team_page_2.professors.count(), 1, str(serializer_team_page_2.errors))
        self.assertIn(new_professor.id, team_page_2_professors, str(serializer_team_page_2.errors))

    def test_update_order_used_by_old_professor(self):
        data = {
            'fullName': 'First Professor',
            'image': self.professor_image.id,
            'year_experience': '6 ans',
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6'
        }

        serializer_first_professor = ProfessorSerializer(data=data)
        self.assertTrue(serializer_first_professor.is_valid(), str(serializer_first_professor.errors))
        first_professor = serializer_first_professor.save()

        team_page = TeamPage.objects.create(professorsTitle='Team Page')

        serializer_team_page = TeamPageSerializer(
            instance=team_page,
            data={'professors': [first_professor.id]}
        )
        self.assertTrue(serializer_team_page.is_valid(), str(serializer_team_page.errors))
        serializer_team_page.save()
        team_page.refresh_from_db()

        team_page_professors = team_page.professors.values_list('id', flat=True)
        self.assertEqual(team_page.professors.count(), 1, str(serializer_team_page.errors))
        self.assertIn(first_professor.id, team_page_professors, str(serializer_team_page.errors))

        data = {
            'fullName': 'New Professor',
            'image': self.professor_image.id,
            'year_experience': '6 ans',
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6'
        }

        serializer_new_professor = ProfessorSerializer(data=data)
        self.assertTrue(serializer_new_professor.is_valid(), str(serializer_new_professor.errors))
        new_professor = serializer_new_professor.save()

        serializer_team_page = TeamPageSerializer(
            instance=team_page,
            data={'professors': [new_professor.id]}
        )
        self.assertTrue(serializer_team_page.is_valid(), str(serializer_team_page.errors))
        serializer_team_page.save()
        team_page.refresh_from_db()

        team_page_professors = team_page.professors.values_list('id', flat=True)
        self.assertEqual(team_page.professors.count(), 1, str(serializer_team_page.errors))
        self.assertIn(new_professor.id, team_page_professors, str(serializer_team_page.errors))

    def test_update_order_of_professor_saved_in_team_page(self):
        data = {
            'fullName': 'First Professor',
            'image': self.professor_image.id,
            'year_experience': '6 ans',
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6',
            'order': 67
        }

        serializer_first_professor = ProfessorSerializer(data=data)
        self.assertTrue(serializer_first_professor.is_valid(), str(serializer_first_professor.errors))
        first_professor = serializer_first_professor.save()

        team_page = TeamPage.objects.create(professorsTitle='Team Page')
        team_page.professors.set([first_professor])

        data = {
            'fullName': 'New Professor',
            'image': self.professor_image.id,
            'year_experience': '6 ans',
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6',
            'order': 68
        }

        serializer_new_professor = ProfessorSerializer(data=data)
        self.assertTrue(serializer_new_professor.is_valid(), str(serializer_new_professor.errors))
        new_professor = serializer_new_professor.save()

        serializer_team_page = TeamPageSerializer(
            instance=team_page,
            data={'professors': [first_professor.id, new_professor.id]}
        )
        self.assertTrue(serializer_team_page.is_valid(), str(serializer_team_page.errors))
        serializer_team_page.save()
        team_page.refresh_from_db()

        data = {
            'order': 67
        }

        serializer_update_professor = ProfessorSerializer(instance=new_professor, data=data, partial=True)
        self.assertTrue(serializer_update_professor.is_valid(), str(serializer_update_professor.errors))

        with self.assertRaises(
                ValidationError,
                msg='Save should failed on Professor.clean with error : '
                    f'Order [{data['order']}] of Professor [{new_professor.fullName}]'
                    f' already used by another Professor in the Team page "{team_page.professorsTitle}" .'
        ) as _exception:
            serializer_update_professor.save()

        self.assertEqual(
            f'Order [{data['order']}] of Professor [{new_professor.fullName}]'
            f' already used by another Professor in the Team page "{team_page.professorsTitle}" .',
            _exception.exception.message_dict['order'][0]
        )

    def test_order_already_used_at_page_creation(self):
        data = {
            'fullName': 'First Professor',
            'image': self.professor_image.id,
            'year_experience': '6 ans',
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6',
            'order': 67
        }

        serializer_first_professor = ProfessorSerializer(data=data)
        self.assertTrue(serializer_first_professor.is_valid(), str(serializer_first_professor.errors))
        first_professor = serializer_first_professor.save()

        team_page = TeamPage.objects.create(professorsTitle='Team Page')
        team_page.professors.set([first_professor])

        data = {
            'fullName': 'New Professor',
            'image': self.professor_image.id,
            'year_experience': '6 ans',
            'role': 'Test User',
            'diploma': 'DE',
            'best_rank': '2/6',
            'order': 67
        }

        serializer_new_professor = ProfessorSerializer(data=data)
        self.assertTrue(serializer_new_professor.is_valid(), str(serializer_new_professor.errors))
        new_professor = serializer_new_professor.save()

        data_team_page = {'professorsTitle': 'Team Page', 'professors': [first_professor.id, new_professor.id]}
        serializer_team_page = TeamPageSerializer(
            data=data_team_page
        )
        self.assertTrue(serializer_team_page.is_valid(), str(serializer_team_page.errors))

        with self.assertRaises(
                ValidationError,
                msg='Save should failed on Professor.clean with error : '
                    f'Order [{data['order']}] of Professor [{first_professor.fullName}]'
                    f' already used by another Professor in the Team page "{data_team_page['professorsTitle']}" .'
        ) as _exception:
            serializer_team_page.save()

        self.assertEqual(
            f'Order [{data['order']}] of Professor [{first_professor.fullName}]'
            f' already used by another Professor in the Team page "{data_team_page['professorsTitle']}" .',
            _exception.exception.message_dict['order'][0]
        )
