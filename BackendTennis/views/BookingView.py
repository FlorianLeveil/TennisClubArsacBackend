from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Booking
from BackendTennis.serializers.BookingSerializer import BookingSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class BookingView(APIView):
    @staticmethod
    def get(request, id=None):
        if id:
            result = get_object_or_404(Booking, id=id)
            serializers = BookingSerializer(result)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        result = Booking.objects.all()
        serializers = BookingSerializer(result, many=True)
        return Response({'status': 'success', "data": serializers.data}, status=200)
    
    
    @staticmethod
    def post(request):
        serializer = BookingSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer)
    
    
    @staticmethod
    def patch(request, id):
        result = get_object_or_404(Booking, id=id)
        serializer = BookingSerializer(result, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer)
    
    
    @staticmethod
    def delete(request, id):
        result = get_object_or_404(Booking, id=id)
        result.delete()
        return Response({"status": "success", "data": "Booking Deleted"})
