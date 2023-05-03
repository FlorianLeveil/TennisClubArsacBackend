import os

from rest_framework import status
from rest_framework.generics import (get_object_or_404)
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Sponsor
from BackendTennis.serializers import SponsorSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return, move_deleted_image_to_new_path


class SponsorView(APIView):
    def get(self, request, id=None):
        if id:
            result = get_object_or_404(Sponsor, id=id)
            serializers = SponsorSerializer(result)
            print(serializers.data)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        result = Sponsor.objects.all()
        serializers = SponsorSerializer(result, many=True)
        return Response({'status': 'success', "data": serializers.data}, status=200)

    def post(self, request):
        serializer = SponsorSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer)

    def patch(self, request, id):
        result = get_object_or_404(Sponsor, id=id)
        serializer = SponsorSerializer(result, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer)

    def delete(self, request, id):
        result = get_object_or_404(Sponsor, id=id)
        move_deleted_image_to_new_path(result)
        result.delete()
        return Response({"status": "success", "data": "Record Deleted"})
