from rest_framework.generics import (get_object_or_404)
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Sponsor
from BackendTennis.serializers import SponsorSerializer
from BackendTennis.serializers.SponsorSerializer import SponsorDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class SponsorView(APIView):
    def get(self, request, id=None, *args, **kwargs):
        if id:
            result = get_object_or_404(Sponsor, id=id)
            serializers = SponsorDetailSerializer(result)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        result = Sponsor.objects.all()
        serializers = SponsorDetailSerializer(result, many=True)
        return Response({'status': 'success', "data": serializers.data}, status=200)
    
    
    def post(self, request):
        serializer = SponsorSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, SponsorDetailSerializer)
    
    
    def patch(self, request, id):
        result = get_object_or_404(Sponsor, id=id)
        serializer = SponsorSerializer(result, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, SponsorDetailSerializer)
    
    
    def delete(self, request, id):
        result = get_object_or_404(Sponsor, id=id)
        result.delete()
        return Response({"status": "success", "data": "Sponsor Deleted"})
