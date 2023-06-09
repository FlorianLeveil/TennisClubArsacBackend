from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Tag
from BackendTennis.pagination import TagPagination
from BackendTennis.serializers import TagSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return, move_deleted_image_to_new_path


class TagView(APIView):
    @staticmethod
    def get(request, id=None):
        if id:
            result = get_object_or_404(Tag, id=id)
            serializers = TagSerializer(result)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        result = Tag.objects.all()
        page_size = request.query_params.get("page_size")
        page = request.query_params.get("page")
        
        if page or (page_size or not page_size == "all"):
            paginator = TagPagination()
            result = paginator.paginate_queryset(result, request)
            serializer = TagSerializer(result, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = TagSerializer(result, many=True)
            return Response({'status': 'success', 'count': result.count(), 'data': serializer.data})
    
    
    @staticmethod
    def post(request):
        serializer = TagSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer)
    
    
    @staticmethod
    def patch(request, id):
        result = get_object_or_404(Tag, id=id)
        serializer = TagSerializer(result, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer)
    
    
    @staticmethod
    def delete(request, id):
        result = get_object_or_404(Tag, id=id)
        result.delete()
        return Response({"status": "success", "data": "Tag Deleted"})
