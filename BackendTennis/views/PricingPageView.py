from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.models import PricingPage
from BackendTennis.permissions.page_permission.pricing_page_permissions import PricingPagePermissions
from BackendTennis.serializers import PricingPageSerializer, PricingPageDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return


class PricingPageListCreateView(ListCreateAPIView):
    queryset = PricingPage.objects.all()
    serializer_class = PricingPageSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [PricingPagePermissions]

    @extend_schema(
        summary='Get list of PricingPage',
        parameters=[],
        responses={200: PricingPageDetailSerializer(many=True)},
        tags=['PricingPages']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a new PricingPage',
        request=serializer_class,
        responses={201: PricingPageDetailSerializer()},
        tags=['PricingPages']
    )
    def post(self, request, *args, **kwargs):
        serializer = PricingPageSerializer(data=request.data)
        return check_if_is_valid_save_and_return(serializer, PricingPageDetailSerializer, is_creation=True)


class PricingPageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = PricingPage.objects.all()
    serializer_class = PricingPageSerializer
    serializer_class_response = PricingPageDetailSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [PricingPagePermissions]

    @extend_schema(
        summary='Get PricingPage with Id',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['PricingPages']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update an PricingPage',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['PricingPages']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Update an PricingPage',
        responses={200: serializer_class_response},
        request=serializer_class,
        tags=['PricingPages']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Delete an PricingPage',
        responses={204: None},
        tags=['PricingPages']
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
