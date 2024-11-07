from django.utils.dateparse import parse_datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import Tournament
from BackendTennis.pagination import TournamentPagination
from BackendTennis.permissions.tournament_permissions import TournamentPermissions
from BackendTennis.serializers import TournamentSerializer, TournamentDetailSerializer
from BackendTennis.utils.utils import check_if_is_valid_save_and_return


class TournamentListCreateView(ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    pagination_class = TournamentPagination
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [TournamentPermissions]

    @extend_schema(
        summary='Get a list of tournaments',
        parameters=[
            OpenApiParameter(name='start_date', description='Start date to return tournaments', required=False,
                             type=int),
            OpenApiParameter(name='end_date', description='End date to return tournaments', required=False,
                             type=int),
        ],
        responses={200: TournamentDetailSerializer(many=True)},
        tags=['Tournaments']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            start_date = parse_datetime(start_date)
        if end_date:
            end_date = parse_datetime(end_date)

        if start_date and end_date:
            queryset = queryset.filter(start__lte=end_date, end__gte=start_date)
        elif start_date:
            queryset = queryset.filter(end__gte=start_date)
        elif end_date:
            queryset = queryset.filter(start__lte=end_date)

        return queryset

    @extend_schema(
        summary='Create a new tournament',
        request=TournamentSerializer,
        responses={201: TournamentDetailSerializer},
        tags=['Tournaments']
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TournamentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    serializer_class_response = TournamentDetailSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [TournamentPermissions]

    @extend_schema(
        summary='Get Tournament by Id',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['Tournaments']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a Tournament',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['Tournaments']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Update a Tournament',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['Tournaments']
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TournamentSerializer(instance, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, TournamentDetailSerializer)

    @extend_schema(
        summary='Delete a Tournament',
        responses={204: None},
        tags=['Tournaments']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
