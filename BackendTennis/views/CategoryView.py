from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from BackendTennis.models import Category
from BackendTennis.permissions.category_permissions import CategoryPermissions
from BackendTennis.serializers import CategorySerializer


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermissions]

    def get_queryset(self):
        return Category.objects.all().order_by('name')

    @extend_schema(
        summary="Get a list of categories",
        responses={200: CategorySerializer(many=True)},
        request=CategorySerializer,
        tags=['Categories']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new category",
        responses={201: CategorySerializer()},
        request=CategorySerializer,
        tags=['Categories']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
    permission_classes = [CategoryPermissions]

    @extend_schema(
        summary="Get category with Id",
        responses={200: CategorySerializer()},
        request=CategorySerializer,
        tags=['Categories']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a category",
        responses={200: CategorySerializer()},
        request=CategorySerializer,
        tags=['Categories']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Update a category",
        responses={200: CategorySerializer()},
        request=CategorySerializer,
        tags=['Categories']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a category",
        responses={204: None},
        tags=['Categories']
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
