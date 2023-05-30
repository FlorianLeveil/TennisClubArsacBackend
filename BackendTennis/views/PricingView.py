from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Pricing
from BackendTennis.serializers import PricingSerializer
from BackendTennis.serializers.PricingSerializer import PricingDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class PricingView(APIView):
    @staticmethod
    def get(request, id=None, *args, **kwargs):
        if id:
            result = get_object_or_404(Pricing, id=id)
            serializers = PricingDetailSerializer(result)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        result = Pricing.objects.all()
        serializers = PricingDetailSerializer(result, many=True)
        return Response({'status': 'success', "data": serializers.data}, status=200)
    
    
    @staticmethod
    def post(request):
        serializer = PricingSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, PricingDetailSerializer)
    
    
    @staticmethod
    def patch(request, id):
        result = get_object_or_404(Pricing, id=id)
        serializer = PricingSerializer(result, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, PricingDetailSerializer)
    
    
    @staticmethod
    def delete(request, id):
        result = get_object_or_404(Pricing, id=id)
        result.delete()
        return Response({"status": "success", "data": "Pricing Deleted"})
