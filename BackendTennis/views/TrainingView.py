from django.utils.dateparse import parse_datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import Training
from BackendTennis.pagination import TrainingPagination
from BackendTennis.permissions.training_permissions import TrainingPermissions
from BackendTennis.serializers import TrainingSerializer, TrainingDetailSerializer
from BackendTennis.utils.utils import check_if_is_valid_save_and_return


class TrainingListCreateView(ListCreateAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    pagination_class = TrainingPagination
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [TrainingPermissions]

    @extend_schema(
        summary="Get a list of trainings",
        parameters=[
            OpenApiParameter(name='start_date', description='Start date to return trainings', required=False,
                             type=int),
            OpenApiParameter(name='end_date', description='End date to return trainings', required=False,
                             type=int),
        ],
        responses={200: TrainingDetailSerializer(many=True)},
        tags=['Trainings']
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
        summary="Create a new training",
        request=TrainingSerializer,
        responses={201: TrainingDetailSerializer},
        tags=['Trainings']
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TrainingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [TrainingPermissions]

    @extend_schema(
        summary="Get Training by Id",
        responses={200: TrainingDetailSerializer()},
        request=serializer_class,
        tags=['Trainings']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a Training",
        responses={200: TrainingDetailSerializer()},
        request=serializer_class,
        tags=['Trainings']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Update a Training",
        responses={200: TrainingDetailSerializer()},
        request=serializer_class,
        tags=['Trainings']
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TrainingSerializer(instance, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, TrainingDetailSerializer)

    @extend_schema(
        summary="Delete a Training",
        responses={204: None},
        tags=['Trainings']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
