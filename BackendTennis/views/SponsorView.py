from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from BackendTennis.models import Sponsor
from BackendTennis.pagination import SponsorPagination
from BackendTennis.serializers import SponsorSerializer, SponsorDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class SponsorListCreateView(ListCreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorDetailSerializer
    pagination_class = SponsorPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Number of results to return per page'),
            openapi.Parameter('page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Page number within the paginated result set'),
        ],
        responses={200: SponsorDetailSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=SponsorSerializer,
        responses={201: SponsorDetailSerializer()},
    )
    def post(self, request, *args, **kwargs):
        serializer = SponsorSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, SponsorDetailSerializer)


class SponsorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorDetailSerializer
    lookup_field = 'id'
