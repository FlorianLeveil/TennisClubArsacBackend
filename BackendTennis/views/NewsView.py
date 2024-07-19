from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from BackendTennis.models import News
from BackendTennis.pagination import NewsPagination
from BackendTennis.serializers import NewsSerializer, NewsDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return

class NewsListCreateView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer
    pagination_class = NewsPagination

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
        ],
        responses={200: NewsDetailSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=NewsSerializer,
        responses={201: NewsDetailSerializer()},
    )
    def post(self, request, *args, **kwargs):
        serializer = NewsSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, NewsDetailSerializer)

class NewsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        request_body=NewsSerializer,
        responses={200: NewsDetailSerializer},
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = NewsSerializer(instance, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, NewsDetailSerializer)

    @swagger_auto_schema(
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"status": "success", "data": "News Deleted"}, status=204)
