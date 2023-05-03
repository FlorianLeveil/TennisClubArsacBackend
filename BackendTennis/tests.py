import datetime

from django.test import TestCase
from django.urls import path, include
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.test import APIRequestFactory, RequestsClient, APITestCase, URLPatternsTestCase
from BackendTennis.models import Booking
from BackendTennis.views import BookingView


class AnimalTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('BackendTennis/', include('BackendTennis.urls')),
    ]
    def setUp(self):
        Booking.objects.create(
            id=1,
            clientFirstName="User1",
            clientLastName="LastName",
            clientEmail="user1@user.fr",
            clientPhoneNumber="0323403204",
            payed=False,
            insurance=False,
            start="2020-11-11",
            end="2020-11-12",
            createAt=datetime.datetime.now().strftime("%Y-%d-%m %H:%M:%S"),
            updateAt=datetime.datetime.now().strftime("%Y-%d-%m %H:%M:%S")
        )

    def test_animals_can_speak(self):
        url = reverse_lazy('BackendTennis:BookingView')
        factory = APIRequestFactory()
        request = factory.get('http://127.0.0.1:8000/Backend/basic/1')
        view = BookingView.as_view()(request)
        # response = view(request)
        print(view.data)
        print(Booking.objects.get(id=1))

        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Booking.objects.count(), 1)
        # self.assertEqual(Booking.objects.get().name, 'DabApps')
# Create your tests here.
