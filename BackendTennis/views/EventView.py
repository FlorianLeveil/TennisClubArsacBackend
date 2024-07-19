from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from datetime import date
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
            raise ValidationError("Bad Mode. Mode available: %s" % ', '.join(Constant.EVENT_MODE.__dict__.values()))

        return queryset


class EventListCreateView(EventModeMixin, generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    pagination_class = EventPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('mode', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Mode of the event',
                              enum=[Constant.EVENT_MODE.HISTORY, Constant.EVENT_MODE.FUTURE_EVENT]),
        ],
        responses={200: EventDetailSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventSerializer
        return EventDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': 'success', 'count': queryset.count(), 'data': serializer.data})

    @swagger_auto_schema(
        request_body=EventSerializer,
        responses={201: EventDetailSerializer()},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, EventDetailSerializer)


class EventRetrieveUpdateDestroyView(EventModeMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        request_body=EventSerializer,
        responses={200: EventDetailSerializer()},
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, EventDetailSerializer)

    @swagger_auto_schema(
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"status": "success", "data": "Event Deleted"})
