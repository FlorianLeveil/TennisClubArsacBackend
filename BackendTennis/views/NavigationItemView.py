from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import NavigationItem
from BackendTennis.permissions.navigation_item_permissions import NavigationItemPermissions
from BackendTennis.serializers import NavigationItemSerializer, NavigationItemDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class NavigationItemListCreateView(ListCreateAPIView):
    queryset = NavigationItem.objects.all()
    serializer_class = NavigationItemSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [NavigationItemPermissions]

    @extend_schema(
        summary='Get list of MenuItem',
        parameters=[],
        responses={200: NavigationItemDetailSerializer(many=True)},
        tags=['MenuItems']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new MenuItem',
        request=serializer_class,
        responses={201: NavigationItemDetailSerializer()},
        tags=['MenuItems']
    )
    def post(self, request, *args, **kwargs):
        serializer = NavigationItemSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, NavigationItemDetailSerializer, is_creation=True)


class NavigationItemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = NavigationItem.objects.all()
    serializer_class = NavigationItemSerializer
    serializer_class_response = NavigationItemDetailSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [NavigationItemPermissions]

    @extend_schema(
        summary='Get MenuItem with Id',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['MenuItems']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a MenuItem',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['MenuItems']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Update a MenuItem',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['MenuItems']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a MenuItem',
        responses={204: None},
        tags=['MenuItems']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
