from datetime import datetime

from django.db.models import Q, Count
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Image
from BackendTennis.pagination import ImagePagination
from BackendTennis.serializers import ImageSerializer
from BackendTennis.serializers.ImageSerializer import ImageDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return, move_deleted_image_to_new_path
from BackendTennis.validators import validate_image_type


class ImageView(APIView):
    def get(self, request, id=None):
        if id:
            result = get_object_or_404(Image, id=id)
            serializer = ImageDetailSerializer(result)
            return Response({'status': 'success', "data": serializer.data}, status=200)
        tags = request.query_params.get("tags").split(",") if request.query_params.get("tags") else None
        page_size = request.query_params.get("page_size")
        page = request.query_params.get("page")
        image_type = request.query_params.get("type")
        end = request.query_params.get("end")
        start = request.query_params.get("start")
        
        result = Image.objects.all()
        
        if image_type:
            validate_image_type(image_type)
            result = result.filter(type=image_type)
        if tags:
            result = result.filter(tags__name__in=tags).annotate(
                    tag_count=Count('tags__name')).filter(tag_count=len(tags))
        if start:
            result = result.filter(createAt__gte=datetime.strptime(start, "%d-%m-%Y").strftime("%Y-%m-%d"))
        if end:
            result = result.filter(createAt__lte=datetime.strptime(end, "%d-%m-%Y").strftime("%Y-%m-%d"))
    
        result = result.order_by('createAt')
        return self._return_with_pagination_if_needed(result, page, page_size, request)

    @staticmethod
    def _return_with_pagination_if_needed(result, page, page_size, request):
        if page or (page_size or not page_size == "all"):
            paginator = ImagePagination()
            result = paginator.paginate_queryset(result, request)
            serializer = ImageDetailSerializer(result, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = ImageDetailSerializer(result, many=True)
            return Response({'status': 'success', 'count': result.count(), 'data': serializer.data})

    @staticmethod
    def post(request):
        serializer = ImageSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, ImageDetailSerializer)

    @staticmethod
    def patch(request, id):
        result = get_object_or_404(Image, id=id)
        serializer = ImageSerializer(result, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, ImageDetailSerializer)

    @staticmethod
    def delete(request, id):
        result = get_object_or_404(Image, id=id)
        move_deleted_image_to_new_path(result)
        result.delete()
        return Response({"status": "success", "data": "Image Deleted"})
