from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import HomePage
from BackendTennis.permissions.page_permission.home_page_permissions import HomePagePermissions
from BackendTennis.serializers import HomePageSerializer, HomePageDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class HomePageListCreateView(ListCreateAPIView):
    queryset = HomePage.objects.all()
    serializer_class = HomePageSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [HomePagePermissions]

    @extend_schema(
        summary='Get list of HomePage',
        parameters=[],
        responses={200: HomePageDetailSerializer(many=True)},
        tags=['HomePages']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new HomePage',
        request=serializer_class,
        responses={201: HomePageDetailSerializer()},
        tags=['HomePages']
    )
    def post(self, request, *args, **kwargs):
        serializer = HomePageSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, HomePageDetailSerializer, is_creation=True)


class HomePageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = HomePage.objects.all()
    serializer_class = HomePageSerializer
    serializer_class_response = HomePageDetailSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [HomePagePermissions]

    @extend_schema(
        summary='Get HomePage with Id',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['HomePages']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update an HomePage',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['HomePages']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Update an HomePage',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['HomePages']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Delete an HomePage',
        responses={204: None},
        tags=['HomePages']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
