from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Sponsor
from BackendTennis.serializers import SponsorSerializer, SponsorDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class SponsorView(APIView):
    @staticmethod
    def get(request, id=None, *args, **kwargs):
        if id:
            result = get_object_or_404(Sponsor, id=id)
            serializers = SponsorDetailSerializer(result)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        result = Sponsor.objects.all()
        serializers = SponsorDetailSerializer(result, many=True)
        return Response({'status': 'success', "data": serializers.data}, status=200)
    
    
    @staticmethod
    def post(request):
        serializer = SponsorSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, SponsorDetailSerializer)
    
    
    @staticmethod
    def patch(request, id):
        result = get_object_or_404(Sponsor, id=id)
        serializer = SponsorSerializer(result, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, SponsorDetailSerializer)
    
    
    @staticmethod
    def delete(request, id):
        result = get_object_or_404(Sponsor, id=id)
        result.delete()
        return Response({"status": "success", "data": "Sponsor Deleted"})
