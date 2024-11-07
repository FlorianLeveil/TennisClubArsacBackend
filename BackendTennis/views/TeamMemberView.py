from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import TeamMember
from BackendTennis.pagination import TeamMemberPagination
from BackendTennis.permissions.team_member_permissions import TeamMemberPermissions
from BackendTennis.serializers import TeamMemberSerializer, TeamMemberDetailSerializer
from BackendTennis.utils.utils import check_if_is_valid_save_and_return


class TeamMemberListCreateView(ListCreateAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    pagination_class = TeamMemberPagination
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [TeamMemberPermissions]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TeamMemberDetailSerializer
        return TeamMemberSerializer

    @extend_schema(
        summary='Get list of Team Member',
        parameters=[
            OpenApiParameter(name='page_size', description='Number of results to return per page', required=False,
                             type=int),
            OpenApiParameter(name='page', description='Page number within the paginated result set', required=False,
                             type=int),
        ],
        responses={200: TeamMemberDetailSerializer(many=True)},
        tags=['TeamMembers']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new Team Member',
        request=serializer_class,
        responses={201: TeamMemberDetailSerializer()},
        tags=['TeamMembers']
    )
    def post(self, request, *args, **kwargs):
        serializer = TeamMemberSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, TeamMemberDetailSerializer, is_creation=True)


class TeamMemberRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    serializer_class_response = TeamMemberDetailSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [TeamMemberPermissions]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TeamMemberDetailSerializer
        return TeamMemberSerializer

    @extend_schema(
        summary='Get Team Member with Id',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['TeamMembers']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a Team Member',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['TeamMembers']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Update a Team Member',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['TeamMembers']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a Team Member',
        responses={204: None},
        tags=['TeamMembers']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
