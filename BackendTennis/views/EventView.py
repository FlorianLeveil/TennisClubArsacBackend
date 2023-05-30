from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date

from BackendTennis.constant import Constant
from BackendTennis.models import Event
from BackendTennis.serializers import EventSerializer, EventDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class EventView(APIView):
    @staticmethod
    def get(request, id=None, *args, **kwargs):
        if id:
            result = get_object_or_404(Event, id=id)
            serializers = EventDetailSerializer(result)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        mode = request.query_params.get('mode')
        if mode == Constant.EVENT_MODE.HISTORY:
            today = date.today()
            events = Event.objects.filter(end__lt=today)
            result = events.order_by('end')
        elif mode == Constant.EVENT_MODE.FUTURE_EVENT:
            today = date.today()
            events = Event.objects.filter(end__gte=today)
            result = events.order_by('start')
        else:
            result = Event.objects.all()
        serializers = EventDetailSerializer(result, many=True)
        return Response({'status': 'success', "data": serializers.data}, status=200)
    
    
    @staticmethod
    def post(request):
        serializer = EventSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, EventDetailSerializer)
    
    
    @staticmethod
    def patch(request, id):
        result = get_object_or_404(Event, id=id)
        serializer = EventSerializer(result, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, EventDetailSerializer)
    
    
    @staticmethod
    def delete(request, id):
        result = get_object_or_404(Event, id=id)
        result.delete()
        return Response({"status": "success", "data": "Event Deleted"})
