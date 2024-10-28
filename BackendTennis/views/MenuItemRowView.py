from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import MenuItemRow
from BackendTennis.permissions.menu_item_row_permissions import MenuItemRowPermissions
from BackendTennis.serializers import MenuItemRowSerializer, MenuItemRowDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class MenuItemRowListCreateView(ListCreateAPIView):
    queryset = MenuItemRow.objects.all()
    serializer_class = MenuItemRowSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [MenuItemRowPermissions]

    @extend_schema(
        summary='Get list of MenuItemRow',
        parameters=[],
        responses={200: MenuItemRowDetailSerializer(many=True)},
        tags=['MenuItemRows']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new MenuItemRow',
        request=serializer_class,
        responses={201: MenuItemRowDetailSerializer()},
        tags=['MenuItemRows']
    )
    def post(self, request, *args, **kwargs):
        serializer = MenuItemRowSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, MenuItemRowDetailSerializer, is_creation=True)


class MenuItemRowRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = MenuItemRow.objects.all()
    serializer_class = MenuItemRowSerializer
    serializer_class_response = MenuItemRowDetailSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [MenuItemRowPermissions]

    @extend_schema(
        summary='Get MenuItemRow with Id',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['MenuItemRows']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a MenuItemRow',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['MenuItemRows']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Update a MenuItemRow',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['MenuItemRows']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a MenuItemRow',
        responses={204: None},
        tags=['MenuItemRows']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
