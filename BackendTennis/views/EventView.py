from datetime import date
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from BackendTennis.constant import Constant
from BackendTennis.models import Event
from BackendTennis.pagination import EventPagination
from BackendTennis.serializers import EventSerializer, EventDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class EventModeMixin:
    def get_queryset(self):
        queryset = Event.objects.all()
        mode = self.request.query_params.get('mode')
        today = date.today()

        if mode == Constant.EVENT_MODE.HISTORY:
            return Event.objects.filter(end__lt=today).order_by('end')
        elif mode == Constant.EVENT_MODE.FUTURE_EVENT:
            return Event.objects.filter(end__gte=today).order_by('start')
        elif mode:
            raise ValidationError("Bad Mode. Mode available : %s" % ', '.join(Constant.EVENT_MODE.__dict__.values()))

        return queryset


class EventListCreateView(EventModeMixin, generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    pagination_class = EventPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('mode', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Mode for filtering events',
                              enum=[Constant.EVENT_MODE.HISTORY, Constant.EVENT_MODE.FUTURE_EVENT]),
            openapi.Parameter('page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Number of results to return per page'),
            openapi.Parameter('page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Page number within the paginated result set'),
        ],
        responses={200: EventDetailSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, EventDetailSerializer)


class EventRetrieveUpdateDestroyView(EventModeMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('mode', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Mode for filtering events',
                              enum=[Constant.EVENT_MODE.HISTORY, Constant.EVENT_MODE.FUTURE_EVENT]),
        ],
        responses={200: EventDetailSerializer()},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, EventDetailSerializer)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"status": "success", "data": "Event Deleted"})
