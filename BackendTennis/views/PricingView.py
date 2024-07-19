from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from BackendTennis.models import Pricing
from BackendTennis.pagination import PricingPagination
from BackendTennis.serializers import PricingSerializer
from BackendTennis.serializers.PricingSerializer import PricingDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return
from BackendTennis.validators import validate_pricing_type


class PricingView(ListCreateAPIView):
    queryset = Pricing.objects.all()
    serializer_class = PricingDetailSerializer
    pagination_class = PricingPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                description='Page size for pagination'
            ),
            openapi.Parameter(
                'page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                description='Page number for pagination'
            ),
            openapi.Parameter(
                'type', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                description='Type of the pricing'
            ),
        ],
        responses={200: PricingDetailSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        pricing_type = self.request.query_params.get("type")

        if pricing_type:
            validate_pricing_type(pricing_type)
            queryset = queryset.filter(type=pricing_type)

        return queryset

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the pricing'),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of the pricing'),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Price'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
            },
            required=['name', 'type', 'price', 'description']
        ),
        responses={201: PricingDetailSerializer()},
    )
    def post(self, request, *args, **kwargs):
        serializer = PricingSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, PricingDetailSerializer)


class PricingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Pricing.objects.all()
    serializer_class = PricingDetailSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        request_body=PricingSerializer,
        responses={200: PricingDetailSerializer()},
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PricingSerializer(instance, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, PricingDetailSerializer)

    @swagger_auto_schema(
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"status": "success", "data": "Pricing Deleted"}, status=204)
