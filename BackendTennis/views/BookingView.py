from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from BackendTennis.models import Booking
from BackendTennis.pagination import BookingPagination
from BackendTennis.serializers.BookingSerializer import BookingSerializer


class BookingListCreateView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    pagination_class = BookingPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Number of results to return per page'),
            openapi.Parameter('page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Page number within the paginated result set'),
        ],
        responses={200: BookingSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'
