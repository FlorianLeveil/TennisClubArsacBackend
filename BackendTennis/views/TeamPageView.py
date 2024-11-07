from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import TeamPage
from BackendTennis.permissions.page_permission.team_page_permissions import TeamPagePermissions
from BackendTennis.serializers import TeamPageSerializer, TeamPageDetailSerializer
from BackendTennis.utils.utils import check_if_is_valid_save_and_return


class TeamPageListCreateView(ListCreateAPIView):
    queryset = TeamPage.objects.all()
    serializer_class = TeamPageSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [TeamPagePermissions]

    @extend_schema(
        summary='Get list of Team Page',
        parameters=[],
        responses={200: TeamPageDetailSerializer(many=True)},
        tags=['TeamPages']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new Team Page',
        request=serializer_class,
        responses={201: TeamPageDetailSerializer()},
        tags=['TeamPages']
    )
    def post(self, request, *args, **kwargs):
        serializer = TeamPageSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, TeamPageDetailSerializer, is_creation=True)


class TeamPageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = TeamPage.objects.all()
    serializer_class = TeamPageSerializer
    serializer_class_response = TeamPageDetailSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [TeamPagePermissions]

    @extend_schema(
        summary='Get Team Page with Id',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['TeamPages']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a Team Page',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['TeamPages']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Update a Team Page',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['TeamPages']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a Team Page',
        responses={204: None},
        tags=['TeamPages']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
