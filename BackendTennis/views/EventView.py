from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date

from BackendTennis.constant import Constant
from BackendTennis.models import Event
from BackendTennis.pagination import EventPagination
from BackendTennis.serializers import EventSerializer, EventDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class EventView(APIView):
    def get(self, request, id=None, *args, **kwargs):
        if id:
            result = get_object_or_404(Event, id=id)
            serializers = EventDetailSerializer(result)
            return Response({'status': 'success', "data": serializers.data}, status=200)
        
        mode = request.query_params.get('mode')
        page_size = request.query_params.get('page_size')
        page = request.query_params.get('page')
        today = date.today()
        count = 0
        
        if ((not page and not page_size) or page_size == "all") and not mode:
            queryset = Event.objects.all().order_by('createAt')
            serializer = EventDetailSerializer(queryset, many=True)
            return Response({'status': 'success', 'count': queryset.count(), 'data': serializer.data})
        elif (page or page_size) and not mode and not page_size == "all":
            queryset = Event.objects.all().order_by('createAt')
            count = queryset.count()
            paginator = EventPagination()
            result = paginator.paginate_queryset(queryset, request)
        elif mode == Constant.EVENT_MODE.HISTORY:
            result = self._get_end_lower_than_today(today)
            count = result.count()
            if not page_size == "all":
                paginator = EventPagination()
                result = paginator.paginate_queryset(result, request)
        elif mode == Constant.EVENT_MODE.FUTURE_EVENT:
            result = self._get_end_greater_or_equal_than_today(today)
            count = result.count()
            if not page_size == "all":
                paginator = EventPagination()
                result = paginator.paginate_queryset(result, request)
        else:
            raise ValidationError("Bad Mode. Mode available : %s" % ', '.join(Constant.EVENT_MODE.__dict__.values()))
        serializers = EventDetailSerializer(result, many=True)
        return Response({'status': 'success','count': count, "data": serializers.data}, status=200)
    
    @staticmethod
    def _get_end_lower_than_today(today):
        events = Event.objects.filter(end__lt=today)
        return events.order_by('end')
    
    
    @staticmethod
    def _get_end_greater_or_equal_than_today(today):
        events = Event.objects.filter(end__gte=today)
        return events.order_by('start')
    
    
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
