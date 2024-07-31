from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from BackendTennis.models import Tag
from BackendTennis.pagination import TagPagination
from BackendTennis.serializers import TagSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class TagView(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = TagPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                description='Page size for pagination'
            ),
            openapi.Parameter(
                'page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                description='Page number for pagination'
            ),
            openapi.Parameter(
                'name', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                description='Search by name'
            ),
        ],
        responses={200: TagSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    @swagger_auto_schema(
        request_body=TagSerializer,
        responses={201: TagSerializer()},
    )
    def post(self, request, *args, **kwargs):
        serializer = TagSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, TagSerializer)


class TagRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'
