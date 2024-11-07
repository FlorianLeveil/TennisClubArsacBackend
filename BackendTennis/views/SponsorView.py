from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import Sponsor
from BackendTennis.pagination import SponsorPagination
from BackendTennis.permissions.sponsor_permissions import SponsorPermissions
from BackendTennis.serializers import SponsorSerializer, SponsorDetailSerializer
from BackendTennis.utils.utils import check_if_is_valid_save_and_return


class SponsorListCreateView(ListCreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    pagination_class = SponsorPagination
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [SponsorPermissions]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SponsorDetailSerializer
        return SponsorSerializer

    @extend_schema(
        summary="Get list of sponsor",
        parameters=[
            OpenApiParameter(name='page_size', description='Number of results to return per page', required=False,
                             type=int),
            OpenApiParameter(name='page', description='Page number within the paginated result set', required=False,
                             type=int),
        ],
        responses={200: SponsorDetailSerializer(many=True)},
        tags=['Sponsors']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new sponsor",
        request=serializer_class,
        responses={201: SponsorDetailSerializer()},
        tags=['Sponsors']
    )
    def post(self, request, *args, **kwargs):
        serializer = SponsorSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, SponsorDetailSerializer, is_creation=True)


class SponsorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    serializer_class_response = SponsorDetailSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [SponsorPermissions]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SponsorDetailSerializer
        return SponsorSerializer

    @extend_schema(
        summary="Get sponsor with Id",
        responses={200: SponsorDetailSerializer},
        request=serializer_class,
        tags=['Sponsors']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a sponsor",
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['Sponsors']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Update a sponsor",
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['Sponsors']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a sponsor",
        responses={204: None},
        tags=['Sponsors']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
