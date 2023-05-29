from rest_framework.generics import (get_object_or_404)
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Booking
from BackendTennis.serializers.BookingSerializer import BookingSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class BookingView(APIView):
    def get(self, request, id=None):
        if id:
            result = get_object_or_404(Booking, id=id)
            serializers = BookingSerializer(result)
            print(serializers.data)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        result = Booking.objects.all()
        serializers = BookingSerializer(result, many=True)
        return Response({'status': 'success', "data": serializers.data}, status=200)
    
    
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer)
    
    
    def patch(self, request, id):
        result = get_object_or_404(Booking, id=id)
        serializer = BookingSerializer(result, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer)
    
    
    def delete(self, request):
        result = get_object_or_404(Booking, id=id)
        result.delete()
        return Response({"status": "success", "data": "Booking Deleted"})
