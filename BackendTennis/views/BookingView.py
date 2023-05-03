from rest_framework import status
from rest_framework.generics import (get_object_or_404)
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.models import Booking
from BackendTennis.serializers.BookingSerializer import BookingSerializer


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
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        result = get_object_or_404(Booking, id=id)
        serializer = BookingSerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        result = get_object_or_404(Booking, id=id)
        result.delete()
        return Response({"status": "success", "data": "Record Deleted"})
