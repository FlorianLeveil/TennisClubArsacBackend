from datetime import datetime
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from BackendTennis.models import Image
from BackendTennis.pagination import ImagePagination
from BackendTennis.serializers import ImageSerializer, ImageDetailSerializer
from BackendTennis.utils import check_if_is_valid_save_and_return, move_deleted_image_to_new_path
from BackendTennis.validators import validate_image_type
from BackendTennis.constant import Constant


class ImageView(ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    pagination_class = ImagePagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('type', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Type of the image',
                              enum=[Constant.IMAGE_TYPE.PRICING, Constant.IMAGE_TYPE.NEWS,
                                    Constant.IMAGE_TYPE.EVENTS, Constant.IMAGE_TYPE.SPONSOR,
                                    Constant.IMAGE_TYPE.PICTURE]),
            openapi.Parameter('tags', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Comma-separated list of tags'),
            openapi.Parameter('start', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date',
                              description='Start date for filtering images (format: dd-mm-yyyy)'),
            openapi.Parameter('end', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date',
                              description='End date for filtering images (format: dd-mm-yyyy)'),
        ],
        responses={200: ImageDetailSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.query_params.get("tags")
        image_type = self.request.query_params.get("type")
        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")

        if image_type:
            validate_image_type(image_type)
            if image_type in [Constant.IMAGE_TYPE.PRICING, Constant.IMAGE_TYPE.NEWS,
                              Constant.IMAGE_TYPE.EVENTS, Constant.IMAGE_TYPE.SPONSOR,
                              Constant.IMAGE_TYPE.PICTURE]:
                queryset = queryset.filter(type=image_type)
            else:
                # Handle invalid image type
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

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ImageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        move_deleted_image_to_new_path(instance)
        return self.destroy(request, *args, **kwargs)
