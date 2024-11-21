from __future__ import annotations

import json
from datetime import datetime

from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.constant import constant_image_type_list
from BackendTennis.models import Image
from BackendTennis.pagination import ImagePagination
from BackendTennis.permissions.image_permissions import ImagePermissions
from BackendTennis.serializers import ImageSerializer, ImageDetailSerializer
from BackendTennis.utils.utils import move_deleted_image_to_new_path
from BackendTennis.validators import validate_image_type


class ImageListCreateView(ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    pagination_class = ImagePagination
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [ImagePermissions]

    @extend_schema(
        summary='Get a list of images',
        parameters=[
            OpenApiParameter(name='type', description='Type of the image', required=False, type=str),
            OpenApiParameter(name='tags', description='Comma-separated list of tags', required=False, type=str),
            OpenApiParameter(name='start', description='Start date for filtering images (format: dd-mm-yyyy)',
                             required=False, type=str),
            OpenApiParameter(name='end', description='End date for filtering images (format: dd-mm-yyyy)',
                             required=False, type=str),
        ],
        responses={status.HTTP_200_OK: ImageDetailSerializer(many=True)},
        tags=['Images']
    )
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.query_params.get('tags')
        image_type = self.request.query_params.get('type')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')

        if image_type:
            validate_image_type(image_type)
            if image_type in constant_image_type_list:
                queryset = queryset.filter(type=image_type)
            else:
                queryset = queryset.none()

        if tags:
            tags_list = tags.split(',')
            queryset = queryset.filter(tags__name__in=tags_list).annotate(
                tag_count=Count('tags__name')).filter(tag_count=len(tags_list))

        if start:
            start_date = datetime.strptime(start, '%d-%m-%Y').strftime('%Y-%m-%d')
            queryset = queryset.filter(createAt__gte=start_date)

        if end:
            end_date = datetime.strptime(end, '%d-%m-%Y').strftime('%Y-%m-%d')
            queryset = queryset.filter(createAt__lte=end_date)

        return queryset.order_by('createAt')

    @extend_schema(
        summary='Create a new image',
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
        summary='Get image with Id',
        responses={status.HTTP_200_OK: ImageDetailSerializer()},
        request=serializer_class,
        tags=['Images']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Update a image',
        responses={status.HTTP_200_OK: ImageDetailSerializer()},
        request=serializer_class,
        tags=['Images']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Update a image',
        responses={status.HTTP_200_OK: ImageDetailSerializer()},
        request=serializer_class,
        tags=['Images']
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a image',
        responses={status.HTTP_204_NO_CONTENT: None},
        tags=['Images']
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        move_deleted_image_to_new_path(instance)
        return self.destroy(request, *args, **kwargs)


class ImageBatchDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ImageSerializer
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [ImagePermissions]

    @extend_schema(
        summary='Delete multiple images',
        responses={
            status.HTTP_200_OK: {
                'description': 'Batch deletion result',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                }
            },
            status.HTTP_400_BAD_REQUEST: {
                'description': 'Batch deletion result',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                }
            },
            status.HTTP_207_MULTI_STATUS: {
                'description': 'Batch deletion result',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'failed_ids': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'List of IDs that could not be deleted'
                    }
                }
            }
        },
        tags=['Images']
    )
    def delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not ids:
            return Response(
                {'success': False, 'message': 'No IDs provided.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        failed_ids = []
        for image_id in ids:
            try:
                instance = Image.objects.get(id=image_id)
                move_deleted_image_to_new_path(instance)
                instance.delete()
            except Image.DoesNotExist:
                failed_ids.append(image_id)

        if failed_ids:
            return Response(
                {
                    'success': False,
                    'message': 'Some images could not be deleted.',
                    'failed_ids': failed_ids,
                },
                status=status.HTTP_207_MULTI_STATUS,
            )

        return Response(
            {'success': True, 'message': 'All images deleted successfully.'},
            status=status.HTTP_200_OK,
        )


class BulkImageUploadView(ListCreateAPIView):
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [ImagePermissions]
    serializer_class = ImageSerializer

    @extend_schema(
        summary='Batch create images',
        request=ImageSerializer,
        responses={
            status.HTTP_201_CREATED: ImageDetailSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: {
                'description': 'Validation error',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'errors': {'type': 'array', 'items': {'type': 'string'}}
                }
            }
        },
        tags=['Images']
    )
    def create(self, request, *args, **kwargs):
        files = request.FILES
        try:
            images_data = json.loads(request.data.get('images_data', '[]'))
        except json.JSONDecodeError as e:
            return Response({
                'success': False,
                'message': 'An error occurred',
                'error': f'Invalid images_data format : {e.msg}',
                'created_images': []
            },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not images_data:
            return Response({
                'success': False,
                'message': 'An error occurred',
                'error': 'No image data received.',
                'created_images': []
            }, status=status.HTTP_400_BAD_REQUEST)

        created_images = []
        errors = []
        for image in images_data:
            image_index = image.get('index')
            if image_index is None:
                errors.append(
                    f'Image data should have an index to correspond to image File : [{image.get('title', 'no title')}]')
                continue

            file_from_image = files.get(f'image_{image['index']}')

            if not file_from_image:
                errors.append(f'Image file not found for image with index : [{image_index}]')
                continue

            image['imageUrl'] = files.get(f'image_{image['index']}')
            serializer = self.get_serializer(data=image)
            if serializer.is_valid():
                try:
                    created_image = serializer.save()
                    created_images.append(self.get_serializer(created_image).data)
                except Exception as e:
                    errors.append(f'Error occurred on image save : [{str(e)}]')
            else:
                errors.append(f'Error occurred on image save : [{str(serializer.errors)}]')

        if errors:
            return Response(
                {
                    'success': False,
                    'message': 'Some images could not be uploaded.',
                    'created_images': created_images,
                    'error': '\n'.join(errors),
                },
                status=status.HTTP_207_MULTI_STATUS,
            )

        return Response(
            {
                'success': True,
                'message': 'All images uploaded successfully.',
                'created_images': created_images,
                'error': ''
            },
            status=status.HTTP_201_CREATED,
        )
