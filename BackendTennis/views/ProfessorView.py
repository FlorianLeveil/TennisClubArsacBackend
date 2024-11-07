from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import Professor
from BackendTennis.pagination import ProfessorPagination
from BackendTennis.permissions.professor_permissions import ProfessorPermissions
from BackendTennis.serializers import ProfessorSerializer, ProfessorDetailSerializer
from BackendTennis.utils.utils import check_if_is_valid_save_and_return


class ProfessorListCreateView(ListCreateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    pagination_class = ProfessorPagination
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [ProfessorPermissions]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfessorDetailSerializer
        return ProfessorSerializer

    @extend_schema(
        summary='Get list of Professor',
        parameters=[
            OpenApiParameter(name='page_size', description='Number of results to return per page', required=False,
                             type=int),
            OpenApiParameter(name='page', description='Page number within the paginated result set', required=False,
                             type=int),
        ],
        responses={200: ProfessorDetailSerializer(many=True)},
        tags=['Professors']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new Professor',
        request=serializer_class,
        responses={201: ProfessorDetailSerializer()},
        tags=['Professors']
    )
    def post(self, request, *args, **kwargs):
        serializer = ProfessorSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, ProfessorDetailSerializer, is_creation=True)


class ProfessorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    serializer_class_response = ProfessorDetailSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [ProfessorPermissions]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfessorDetailSerializer
        return ProfessorSerializer

    @extend_schema(
        summary='Get Professor with Id',
        responses={200: ProfessorDetailSerializer},
        request=serializer_class,
        tags=['Professors']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a Professor',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['Professors']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Update a Professor',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['Professors']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a Professor',
        responses={204: None},
        tags=['Professors']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
