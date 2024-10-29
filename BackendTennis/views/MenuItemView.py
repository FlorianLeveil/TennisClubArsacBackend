from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import MenuItem
from BackendTennis.permissions.menu_item_permissions import MenuItemPermissions
from BackendTennis.serializers import MenuItemSerializer, MenuItemDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class MenuItemListCreateView(ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [MenuItemPermissions]

    @extend_schema(
        summary='Get list of MenuItem',
        parameters=[],
        responses={200: MenuItemDetailSerializer(many=True)},
        tags=['MenuItems']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new MenuItem',
        request=serializer_class,
        responses={201: MenuItemDetailSerializer()},
        tags=['MenuItems']
    )
    def post(self, request, *args, **kwargs):
        serializer = MenuItemSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, MenuItemDetailSerializer, is_creation=True)


class MenuItemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    serializer_class_response = MenuItemDetailSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [MenuItemPermissions]

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
