from datetime import datetime

from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.constant import constant_image_type_list
from BackendTennis.models import Image
from BackendTennis.pagination import ImagePagination
from BackendTennis.permissions.image_permissions import ImagePermissions
from BackendTennis.serializers import ImageSerializer, ImageDetailSerializer
from BackendTennis.utils import move_deleted_image_to_new_path
from BackendTennis.validators import validate_image_type


class ImageListCreateView(ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    pagination_class = ImagePagination
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [ImagePermissions]

    @extend_schema(
        summary="Get a list of images",
        parameters=[
            OpenApiParameter(name='type', description='Type of the image', required=False, type=str),
            OpenApiParameter(name='tags', description='Comma-separated list of tags', required=False, type=str),
            OpenApiParameter(name='start', description='Start date for filtering images (format: dd-mm-yyyy)',
                             required=False, type=str),
            OpenApiParameter(name='end', description='End date for filtering images (format: dd-mm-yyyy)',
                             required=False, type=str),
        ],
        responses={200: ImageDetailSerializer(many=True)},
        tags=['Images']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.query_params.get("tags")
        image_type = self.request.query_params.get("type")
        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")

        if image_type:
            validate_image_type(image_type)
            if image_type in constant_image_type_list:
                queryset = queryset.filter(type=image_type)
            else:
                queryset = queryset.none()

        if tags:
            tags_list = tags.split(",")
            queryset = queryset.filter(tags__name__in=tags_list).annotate(
                tag_count=Count('tags__name')).filter(tag_count=len(tags_list))

        if start:
            start_date = datetime.strptime(start, "%d-%m-%Y").strftime("%Y-%m-%d")
            queryset = queryset.filter(createAt__gte=start_date)

        if end:
            end_date = datetime.strptime(end, "%d-%m-%Y").strftime("%Y-%m-%d")
            queryset = queryset.filter(createAt__lte=end_date)

        return queryset.order_by('createAt')

    @extend_schema(
        summary="Create a new image",
        request=ImageSerializer,
        responses={201: ImageDetailSerializer},
        tags=['Images']
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ImageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    lookup_field = 'id'
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [ImagePermissions]

    @extend_schema(
        summary="Get image with Id",
        responses={200: ImageDetailSerializer()},
        request=serializer_class,
        tags=['Images']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a image",
        responses={200: ImageDetailSerializer()},
        request=serializer_class,
        tags=['Images']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Update a image",
        responses={200: ImageDetailSerializer()},
        request=serializer_class,
        tags=['Images']
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a image",
        responses={204: None},
        tags=['Images']
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        move_deleted_image_to_new_path(instance)
        return self.destroy(request, *args, **kwargs)
