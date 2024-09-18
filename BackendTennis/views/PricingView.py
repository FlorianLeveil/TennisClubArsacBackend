from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.constant import constant_pricing_type_list
from BackendTennis.models import Pricing
from BackendTennis.pagination import PricingPagination
from BackendTennis.permissions.pricing_permissions import PricingPermissions
from BackendTennis.serializers import PricingSerializer
from BackendTennis.serializers.PricingSerializer import PricingDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return
from BackendTennis.validators import validate_pricing_type


class PricingListCreateView(ListCreateAPIView):
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer
    pagination_class = PricingPagination
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [PricingPermissions]

    @extend_schema(
        summary="Get a list of pricing",
        parameters=[
            OpenApiParameter(name='page_size', description='Number of results to return per page', required=False,
                             type=int),
            OpenApiParameter(name='page', description='Page number within the paginated result set', required=False,
                             type=int),
            OpenApiParameter(name='type', type=str, description='Type of the pricing', enum=constant_pricing_type_list
                             ),
            OpenApiParameter(name='order', type=str, description='Order of sorting (asc or desc)', enum=['asc', 'desc']
                             ),
        ],
        responses={200: PricingDetailSerializer(many=True)},
        tags=['Pricings']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        pricing_type = self.request.query_params.get("type")
        order = self.request.query_params.get("order")

        if pricing_type:
            validate_pricing_type(pricing_type)
            queryset = queryset.filter(type=pricing_type)

        if order == 'asc':
            queryset = queryset.order_by('price')
        elif order == 'desc':
            queryset = queryset.order_by('-price')

        return queryset

    @extend_schema(
        summary="Create a new pricing",
        request=serializer_class,
        responses={201: PricingDetailSerializer()},
        tags=['Pricings']
    )
    def post(self, request, *args, **kwargs):
        serializer = PricingSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, PricingDetailSerializer, is_creation=True)


class PricingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [PricingPermissions]

    @extend_schema(
        summary="Get pricing with Id",
        responses={200: PricingDetailSerializer()},
        request=serializer_class,
        tags=['Pricings']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a pricing",
        request=serializer_class,
        responses={200: PricingDetailSerializer()},
        tags=['Pricings']
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PricingSerializer(instance, data=request.data, partial=True)
        return check_if_is_valid_save_and_return(serializer, PricingDetailSerializer)

    @extend_schema(
        summary="Update a pricing",
        responses={200: PricingDetailSerializer()},
        request=serializer_class,
        tags=['Pricings']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a pricing",
        responses={204: None},
        tags=['Pricings']
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"status": "success", "data": "Pricing Deleted"}, status=204)
