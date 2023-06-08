from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Category
from BackendTennis.pagination import CategoryPagination
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
        page_size = request.query_params.get("page_size")
        page = request.query_params.get("page")
    
        if page or (page_size or not page_size == "all"):
            paginator = CategoryPagination()
            result = paginator.paginate_queryset(result, request)
            serializer = CategorySerializer(result, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = CategorySerializer(result, many=True)
            return Response({'status': 'success', 'count': result.count(), 'data': serializer.data})


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
