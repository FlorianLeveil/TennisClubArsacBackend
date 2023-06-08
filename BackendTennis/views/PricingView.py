from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Pricing
from BackendTennis.pagination import PricingPagination
from BackendTennis.serializers import PricingSerializer
from BackendTennis.serializers.PricingSerializer import PricingDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return
from BackendTennis.validators import validate_pricing_type


class PricingView(APIView):
    @staticmethod
    def get(request, id=None):
        if id:
            result = get_object_or_404(Pricing, id=id)
            serializers = PricingSerializer(result)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        result = Pricing.objects.all()
        page_size = request.query_params.get("page_size")
        page = request.query_params.get("page")
        pricing_type = request.query_params.get("type")
        
        
        if pricing_type:
            validate_pricing_type(pricing_type)
            result = result.filter(type=pricing_type)
        if page or (page_size or not page_size == "all"):
            paginator = PricingPagination()
            result = paginator.paginate_queryset(result, request)
            serializer = PricingSerializer(result, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = PricingSerializer(result, many=True)
            return Response({'status': 'success', 'count': result.count(), 'data': serializer.data})
    
    
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
