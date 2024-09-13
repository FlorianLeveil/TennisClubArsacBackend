from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import Booking
from BackendTennis.pagination import BookingPagination
from BackendTennis.permissions.booking_permissions import BookingPermissions
from BackendTennis.serializers.BookingSerializer import BookingSerializer


class BookingListCreateView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    pagination_class = BookingPagination
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [BookingPermissions]

    def get_queryset(self):
        return Booking.objects.all().order_by('createAt')

    @extend_schema(
        summary="Get a list of bookings",
        parameters=[
            OpenApiParameter(name='page_size', description='Number of results to return per page', required=False,
                             type=int),
            OpenApiParameter(name='page', description='Page number within the paginated result set', required=False,
                             type=int),
        ],
        responses={200: BookingSerializer(many=True)},
        tags=['Bookings']

    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new booking",
        request=serializer_class,
        responses={201: BookingSerializer},
        tags=['Bookings']
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [BookingPermissions]

    @extend_schema(
        summary="Get booking with Id",
        responses={200: BookingSerializer()},
        request=serializer_class,
        tags=['Bookings']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a booking",
        responses={200: BookingSerializer()},
        request=serializer_class,
        tags=['Bookings']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Update a booking",
        responses={200: BookingSerializer()},
        request=serializer_class,
        tags=['Bookings']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a booking",
        responses={204: None},
        tags=['Bookings']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
