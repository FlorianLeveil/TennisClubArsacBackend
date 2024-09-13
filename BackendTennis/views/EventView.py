from datetime import date

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.constant import Constant, constant_event_mode_list
from BackendTennis.models import Event
from BackendTennis.pagination import EventPagination
from BackendTennis.permissions.event_permissions import EventPermissions
from BackendTennis.serializers import EventSerializer, EventDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class EventModeMixin:
    def __init__(self):
        self.request = None

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


class EventListCreateView(EventModeMixin, ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    pagination_class = EventPagination
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [EventPermissions]

    @extend_schema(
        summary="Get a list of events",
        parameters=[
            OpenApiParameter(name='mode', required=True, type=str, description='Mode of the event',
                             enum=constant_event_mode_list),
        ],
        responses={200: EventDetailSerializer(many=True)},
        tags=['Events']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
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

    @extend_schema(
        summary="Create a new event",
        request=EventSerializer,
        responses={201: EventDetailSerializer()},
        tags=['Events']
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, EventDetailSerializer)


class EventRetrieveUpdateDestroyView(EventModeMixin, RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [EventPermissions]

    @extend_schema(
        summary="Get event with Id",
        responses={200: EventDetailSerializer()},
        request=serializer_class,
        tags=['Events']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a event",
        request=serializer_class,
        responses={200: EventDetailSerializer()},
        tags=['Events']
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, EventDetailSerializer)

    @extend_schema(
        summary="Update a event",
        responses={200: EventDetailSerializer()},
        request=serializer_class,
        tags=['Events']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a event",
        responses={204: None},
        tags=['Events']
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"status": "success", "data": "Event Deleted"})
