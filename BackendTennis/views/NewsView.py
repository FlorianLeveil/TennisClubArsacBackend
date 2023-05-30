from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import News
from BackendTennis.serializers import NewsSerializer, NewsDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class NewsView(APIView):
    @staticmethod
    def get(request, id=None, *args, **kwargs):
        if id:
            result = get_object_or_404(News, id=id)
            serializers = NewsDetailSerializer(result)
            return Response({'status': 'success', "data": serializers.data}, status=200)        
        news = News.objects.all()
        result = news.order_by('createAt')
        serializers = NewsDetailSerializer(result, many=True)
        return Response({'status': 'success', "data": serializers.data}, status=200)
    
    
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
