from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Sponsor
from BackendTennis.pagination import SponsorPagination
from BackendTennis.serializers import SponsorSerializer, SponsorDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class SponsorView(APIView):
    @staticmethod
    def get(request, id=None):
        if id:
            result = get_object_or_404(Sponsor, id=id)
            serializers = SponsorDetailSerializer(result)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        result = Sponsor.objects.all()
        page_size = request.query_params.get("page_size")
        page = request.query_params.get("page")
        
        if page or (page_size or not page_size == "all"):
            paginator = SponsorPagination()
            result = paginator.paginate_queryset(result, request)
            serializer = SponsorDetailSerializer(result, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = SponsorDetailSerializer(result, many=True)
            return Response({'status': 'success', 'count': result.count(), 'data': serializer.data})
    
    
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
