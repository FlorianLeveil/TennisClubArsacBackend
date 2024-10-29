from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import PageRender
from BackendTennis.permissions.page_render_permissions import PageRenderPermissions
from BackendTennis.serializers import PageRenderSerializer, PageRenderDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class PageRenderListCreateView(ListCreateAPIView):
    queryset = PageRender.objects.all()
    serializer_class = PageRenderSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [PageRenderPermissions]

    @extend_schema(
        summary='Get list of PageRender',
        parameters=[],
        responses={200: PageRenderDetailSerializer(many=True)},
        tags=['PageRenders']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new PageRender',
        request=serializer_class,
        responses={201: PageRenderDetailSerializer()},
        tags=['PageRenders']
    )
    def post(self, request, *args, **kwargs):
        serializer = PageRenderSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, PageRenderDetailSerializer, is_creation=True)


class PageRenderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = PageRender.objects.all()
    serializer_class = PageRenderSerializer
    serializer_class_response = PageRenderDetailSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [PageRenderPermissions]

    @extend_schema(
        summary='Get PageRender with Id',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['PageRenders']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a PageRender',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['PageRenders']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Update a PageRender',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['PageRenders']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a PageRender',
        responses={204: None},
        tags=['PageRenders']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
