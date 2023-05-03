import os

from rest_framework import status
from rest_framework.generics import (get_object_or_404)
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Image
from BackendTennis.serializers import ImageSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return, move_deleted_image_to_new_path


class ImageView(APIView):
    def get(self, request, id=None):
        if id:
            result = get_object_or_404(Image, id=id)
            serializers = ImageSerializer(result)
            print(serializers.data)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        result = Image.objects.all()
        serializers = ImageSerializer(result, many=True)
        return Response({'status': 'success', "data": serializers.data}, status=200)

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer)

    def patch(self, request, id):
        result = get_object_or_404(Image, id=id)
        serializer = ImageSerializer(result, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer)

    def delete(self, request, id):
        result = get_object_or_404(Image, id=id)
        move_deleted_image_to_new_path(result)
        result.delete()
        return Response({"status": "success", "data": "Record Deleted"})
