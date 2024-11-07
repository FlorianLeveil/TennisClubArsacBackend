from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import NavigationItem
from BackendTennis.permissions.navigation_item_permissions import NavigationItemPermissions
from BackendTennis.serializers import NavigationItemSerializer, NavigationItemDetailSerializer
from BackendTennis.services.navigation_item_service import update_multiple_navigation_items
from BackendTennis.utils.utils import check_if_is_valid_save_and_return


class NavigationItemListCreateView(ListCreateAPIView):
    queryset = NavigationItem.objects.all()
    serializer_class = NavigationItemSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [NavigationItemPermissions]

    @extend_schema(
        summary='Get list of NavigationItem',
        parameters=[],
        responses={200: NavigationItemDetailSerializer(many=True)},
        tags=['NavigationItems']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new NavigationItem',
        request=serializer_class,
        responses={201: NavigationItemDetailSerializer()},
        tags=['NavigationItems']
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
        summary='Get NavigationItem with Id',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['NavigationItems']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a NavigationItem',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['NavigationItems']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Update a NavigationItem',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['NavigationItems']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a NavigationItem',
        responses={204: None},
        tags=['NavigationItems']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateNavigationItemsView(APIView):
    serializer_class = NavigationItemSerializer
    serializer_class_response = NavigationItemDetailSerializer
    permission_classes = [NavigationItemPermissions]

    @extend_schema(
        summary='Update many NavigationItems',
        responses={200: None},
        request=serializer_class,
        tags=['NavigationItems']
    )
    def patch(self, request):
        navigation_items_updates = request.data.get('updates', [])
        try:
            update_multiple_navigation_items(navigation_items_updates)
            return Response({'status': 'success'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)
