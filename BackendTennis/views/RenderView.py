from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import Render
from BackendTennis.permissions.render_permissions import RenderPermissions
from BackendTennis.serializers import RenderSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class RenderListCreateView(ListCreateAPIView):
    queryset = Render.objects.all()
    serializer_class = RenderSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [RenderPermissions]

    @extend_schema(
        summary='Get list of Render',
        parameters=[],
        responses={200: RenderSerializer(many=True)},
        tags=['Renders']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new Render',
        request=serializer_class,
        responses={201: RenderSerializer()},
        tags=['Renders']
    )
    def post(self, request, *args, **kwargs):
        serializer = RenderSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, RenderSerializer, is_creation=True)


class RenderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Render.objects.all()
    serializer_class = RenderSerializer
    serializer_class_response = RenderSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [RenderPermissions]

    @extend_schema(
        summary='Get Render with Id',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['Renders']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a Render',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['Renders']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Update a Render',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['Renders']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a Render',
        responses={204: None},
        tags=['Renders']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
