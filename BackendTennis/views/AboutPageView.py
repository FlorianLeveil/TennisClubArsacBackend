from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import AboutPage
from BackendTennis.permissions.about_page_permissions import AboutPagePermissions
from BackendTennis.serializers import AboutPageSerializer, AboutPageDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class AboutPageListCreateView(ListCreateAPIView):
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [AboutPagePermissions]

    @extend_schema(
        summary='Get list of About Page',
        parameters=[],
        responses={200: AboutPageDetailSerializer(many=True)},
        tags=['AboutPages']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new About Page',
        request=serializer_class,
        responses={201: AboutPageDetailSerializer()},
        tags=['AboutPages']
    )
    def post(self, request, *args, **kwargs):
        serializer = AboutPageSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, AboutPageDetailSerializer, is_creation=True)


class AboutPageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer
    serializer_class_response = AboutPageDetailSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [AboutPagePermissions]

    @extend_schema(
        summary='Get About Page with Id',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['AboutPages']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update an About Page',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['AboutPages']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Update an About Page',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['AboutPages']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Delete an About Page',
        responses={204: None},
        tags=['AboutPages']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
