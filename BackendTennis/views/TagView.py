from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import Tag
from BackendTennis.pagination import TagPagination
from BackendTennis.permissions.tag_permissions import TagPermissions
from BackendTennis.serializers import TagSerializer
from BackendTennis.utils.utils import check_if_is_valid_save_and_return


class TagView(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = TagPagination
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [TagPermissions]

    @extend_schema(
        summary="Get a list of tag",
        parameters=[
            OpenApiParameter(name='page_size', description='Number of results to return per page', required=False,
                             type=int),
            OpenApiParameter(name='page', description='Page number within the paginated result set', required=False,
                             type=int),
            OpenApiParameter(name='name', type=str, description='Search by name'),
        ],
        responses={200: TagSerializer(many=True)},
        tags=['Tags'],
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset.order_by('name')

    @extend_schema(
        summary="Create a new tag",
        request=TagSerializer,
        responses={201: TagSerializer()},
        tags=['Tags']
    )
    def post(self, request, *args, **kwargs):
        serializer = TagSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, TagSerializer, is_creation=True)


class TagRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [TagPermissions]

    @extend_schema(
        summary="Get tag with Id",
        responses={200: TagSerializer()},
        request=serializer_class,
        tags=['Tags']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a tag",
        responses={200: TagSerializer()},
        request=serializer_class,
        tags=['Tags']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Update a tag",
        responses={200: TagSerializer()},
        request=serializer_class,
        tags=['Tags']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a tag",
        responses={204: None},
        tags=['Tags']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
