from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import ClubValue
from BackendTennis.permissions.club_value_permissions import ClubValuePermissions
from BackendTennis.serializers import ClubValueSerializer


class ClubValueListCreateView(ListCreateAPIView):
    queryset = ClubValue.objects.all()
    serializer_class = ClubValueSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [ClubValuePermissions]

    @extend_schema(
        summary="Get a list of Club Values",
        responses={200: ClubValueSerializer(many=True)},
        request=serializer_class,
        tags=['ClubValues']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new Club Values",
        responses={201: ClubValueSerializer()},
        request=serializer_class,
        tags=['ClubValues']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ClubValueRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ClubValue.objects.all()
    serializer_class = ClubValueSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [ClubValuePermissions]

    @extend_schema(
        summary="Get Club Values with Id",
        responses={200: ClubValueSerializer()},
        request=serializer_class,
        tags=['ClubValues']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a Club Values",
        responses={200: ClubValueSerializer()},
        request=serializer_class,
        tags=['ClubValues']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Update a Club Values",
        responses={200: ClubValueSerializer()},
        request=serializer_class,
        tags=['ClubValues']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a Club Values",
        responses={204: None},
        tags=['ClubValues']
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
