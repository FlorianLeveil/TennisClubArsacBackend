from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import News
from BackendTennis.pagination import NewsPagination
from BackendTennis.serializers import NewsSerializer, NewsDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class NewsView(APIView):
    @staticmethod
    def get(request, id=None, *args, **kwargs):
        if id:
            result = get_object_or_404(News, id=id)
            serializer = NewsDetailSerializer(result)
            return Response({'status': 'success', "data": serializer.data}, status=200)
        elif request.query_params.get('page_size') == 'all':
            queryset = News.objects.all().order_by('createAt')
            serializer = NewsDetailSerializer(queryset, many=True)
            return Response({'status': 'success', 'count': queryset.count(), 'data': serializer.data})
        else:
            paginator = NewsPagination()
            queryset = News.objects.all().order_by('createAt')
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = NewsDetailSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
    
    
    @staticmethod
    def post(request):
        serializer = NewsSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, NewsDetailSerializer)
    
    
    @staticmethod
    def patch(request, id):
        result = get_object_or_404(News, id=id)
        serializer = NewsSerializer(result, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, NewsDetailSerializer)
    
    
    @staticmethod
    def delete(request, id):
        result = get_object_or_404(News, id=id)
        result.delete()
        return Response({"status": "success", "data": "News Deleted"})
