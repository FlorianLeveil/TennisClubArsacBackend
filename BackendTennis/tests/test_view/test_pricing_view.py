from datetime import date
from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_api_key.models import APIKey
from rest_framework_simplejwt.tokens import AccessToken
from BackendTennis.models import User, Pricing, Image
from BackendTennis.serializers import PricingSerializer
from BackendTennis.constant import constant_pricing_type_list


class PricingViewTests(APITestCase):

    def setUp(self):
        # Créer un utilisateur et un superutilisateur pour les tests
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            birthdate=date(1990, 1, 1)
        )
        self.superuser = User.objects.create_superuser(
            email='superuser@example.com',
            password='superpassword',
            first_name='Super',
            last_name='User',
            birthdate=date(1990, 1, 1)
        )

        self.image = Image.objects.create(title="test", type="sponsor")


        # Créer un token JWT pour cet utilisateur et le superutilisateur
        self.token = str(AccessToken.for_user(self.user))
        self.superuser_token = str(AccessToken.for_user(self.superuser))

        # Créer une API key pour les tests
        self.api_key, self.key = APIKey.objects.create_key(name="test-api-key")

        # Créer un prix existant pour les tests
        self.pricing = Pricing.objects.create(
            title='Basic Pricing',
            description='Basic description',
            price=100.0,
            type='regular'
        )

        # URL pour accéder aux vues des pricing
        self.url = '/BackendTennis/pricing/'
        self.detail_url = f'{self.url}{self.pricing.id}/'

    def test_get_pricing_list_with_api_key(self):
        """ Teste la récupération de la liste des pricing avec une API Key """
        response = self.client.get(self.url, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pricings = Pricing.objects.all()
        serializer = PricingSerializer(pricings, many=True)
        self.assertEqual(response.data['data'], serializer.data)
        self.assertEqual(response.data['status'], 'success')

    def test_get_pricing_list_with_invalid_api_key(self):
        """ Teste la récupération de la liste des pricing avec une clé API invalide """
        response = self.client.get(self.url, HTTP_API_KEY="invalid_key")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_pricing_with_jwt_and_api_key(self):
        """ Teste la création d'un pricing avec JWT et API Key """
        data = {
            'title': 'Premium Pricing',
            'description': 'Premium description',
            'price': 200.0,
            'type': 'other',
            'image': self.image.id
        }
        permission = Permission.objects.get(codename='add_pricing')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_pricing_without_jwt(self):
        """ Teste la création d'un pricing sans JWT (doit échouer) """
        data = {
            'title': 'Premium Pricing',
            'description': 'Premium description',
            'price': 200.0,
            'type': 'premium'
        }
        response = self.client.post(self.url, data=data, HTTP_API_KEY=self.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_pricing_with_invalid_type(self):
        data = {
            'title': 'Invalid Pricing',
            'description': 'Invalid description',
            'price': 150.0,
            'type': 'invalid_type',
            'image': self.image.id
        }
        permission = Permission.objects.get(codename='add_pricing')
        self.user.user_permissions.add(permission)
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Bad Type. Type available : other, children, adult', str(response.data))

    def test_superuser_can_create_pricing(self):
        """ Teste que le superutilisateur peut créer un pricing sans permissions explicites """
        data = {
            'title': 'Super Pricing',
            'description': 'Super description',
            'price': 300.0,
            'type': 'other',
            'image': self.image.id
        }
        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_pricing_with_jwt_and_api_key(self):
        """ Teste la mise à jour d'un pricing avec JWT et API Key """
        data = {'price': 150.0}
        permission = Permission.objects.get(codename='change_pricing')
        self.user.user_permissions.add(permission)
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pricing.refresh_from_db()
        self.assertEqual(self.pricing.price, 150.0)

    def test_superuser_can_update_pricing(self):
        """ Teste que le superutilisateur peut mettre à jour un pricing sans permissions explicites """
        data = {'price': 350.0}
        response = self.client.patch(
            self.detail_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pricing.refresh_from_db()
        self.assertEqual(self.pricing.price, 350.0)

    def test_delete_pricing_with_jwt_and_api_key(self):
        """ Teste la suppression d'un pricing avec JWT et API Key """
        permission = Permission.objects.get(codename='delete_pricing')
        self.user.user_permissions.add(permission)
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pricing.objects.count(), 0)

    def test_superuser_can_delete_pricing(self):
        """ Teste que le superutilisateur peut supprimer un pricing sans permissions explicites """
        response = self.client.delete(
            self.detail_url,
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}',
            HTTP_API_KEY=self.key
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pricing.objects.count(), 0)
