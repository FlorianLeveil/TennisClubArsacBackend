from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Image
from BackendTennis.serializers import ImageSerializer
from BackendTennis.serializers.ImageSerializer import ImageDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return, move_deleted_image_to_new_path


class ImageView(APIView):
    @staticmethod
    def get(request, id=None):
        if id:
            result = get_object_or_404(Image, id=id)
            serializers = ImageDetailSerializer(result)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        result = Image.objects.all()
        serializers = ImageDetailSerializer(result, many=True)
        return Response({'status': 'success', "data": serializers.data}, status=200)
    
    
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
