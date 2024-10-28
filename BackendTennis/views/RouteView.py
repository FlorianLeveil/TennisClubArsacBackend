from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import Route
from BackendTennis.permissions.route_permissions import RoutePermissions
from BackendTennis.serializers import RouteSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class RouteListCreateView(ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [RoutePermissions]

    @extend_schema(
        summary='Get list of Route',
        parameters=[],
        responses={200: RouteSerializer(many=True)},
        tags=['Routes']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new Route',
        request=serializer_class,
        responses={201: RouteSerializer()},
        tags=['Routes']
    )
    def post(self, request, *args, **kwargs):
        serializer = RouteSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, RouteSerializer, is_creation=True)


class RouteRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    serializer_class_response = RouteSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [RoutePermissions]

    @extend_schema(
        summary='Get Route with Id',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['Routes']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a Route',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['Routes']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Update a Route',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['Routes']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a Route',
        responses={204: None},
        tags=['Routes']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
