from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import News
from BackendTennis.pagination import NewsPagination
from BackendTennis.permissions.news_permissions import NewsPermissions
from BackendTennis.serializers import NewsSerializer, NewsDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class NewsListCreateView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = NewsPagination
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [NewsPermissions]

    @extend_schema(
        summary="Get a list of news",
        parameters=[
            OpenApiParameter(name='page_size', description='Number of results to return per page', required=False,
                             type=int),
            OpenApiParameter(name='page', description='Page number within the paginated result set', required=False,
                             type=int),
        ],
        responses={200: NewsDetailSerializer(many=True)},
        tags=['News']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new news",
        request=NewsSerializer,
        responses={201: NewsDetailSerializer()},
        tags=['News']
    )
    def post(self, request, *args, **kwargs):
        serializer = NewsSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, NewsDetailSerializer, is_creation=True)


class NewsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [NewsPermissions]

    @extend_schema(
        summary="Get news with Id",
        responses={200: NewsDetailSerializer()},
        request=serializer_class,
        tags=['News']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a news",
        request=NewsSerializer,
        responses={200: NewsDetailSerializer()},
        tags=['News']
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = NewsSerializer(instance, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, NewsDetailSerializer)

    @extend_schema(
        summary="Update a news",
        responses={200: NewsDetailSerializer()},
        request=serializer_class,
        tags=['News']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a news",
        responses={204: None},
        tags=['News']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
