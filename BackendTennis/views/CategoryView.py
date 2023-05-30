from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Category
from BackendTennis.serializers import CategorySerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class CategoryView(APIView):
    @staticmethod
    def get(request, id=None):
        if id:
            result = get_object_or_404(Category, id=id)
            serializers = CategorySerializer(result)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        result = Category.objects.all()
        serializers = CategorySerializer(result, many=True)
        return Response({'status': 'success', "data": serializers.data}, status=200)
    
    
    @staticmethod
    def post(request):
        serializer = CategorySerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer)
    
    
    @staticmethod
    def patch(request, id):
        result = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(result, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer)
    
    
    @staticmethod
    def delete(request, id):
        result = get_object_or_404(Category, id=id)
        result.delete()
        return Response({"status": "success", "data": "Category Deleted"})
