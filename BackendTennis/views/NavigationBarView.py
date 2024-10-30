from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import NavigationBar
from BackendTennis.permissions.navigation_bar_permissions import NavigationBarPermissions
from BackendTennis.serializers import NavigationBarSerializer, NavigationBarDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class NavigationBarListCreateView(ListCreateAPIView):
    queryset = NavigationBar.objects.all()
    serializer_class = NavigationBarSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [NavigationBarPermissions]

    @extend_schema(
        summary='Get list of NavigationBar',
        parameters=[],
        responses={200: NavigationBarDetailSerializer(many=True)},
        tags=['NavigationBars']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new NavigationBar',
        request=serializer_class,
        responses={201: NavigationBarDetailSerializer()},
        tags=['NavigationBars']
    )
    def post(self, request, *args, **kwargs):
        serializer = NavigationBarSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, NavigationBarDetailSerializer, is_creation=True)


class NavigationBarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = NavigationBar.objects.all()
    serializer_class = NavigationBarSerializer
    serializer_class_response = NavigationBarDetailSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [NavigationBarPermissions]

    @extend_schema(
        summary='Get NavigationBar with Id',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['NavigationBars']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a NavigationBar',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['NavigationBars']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Update a NavigationBar',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['NavigationBars']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a NavigationBar',
        responses={204: None},
        tags=['NavigationBars']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
