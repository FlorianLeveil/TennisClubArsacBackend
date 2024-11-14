import datetime
import json
import os

from rest_framework import status
from rest_framework.response import Response


def compute_image_url(instance, filename):
    return os.path.join('images', instance.type, '{}.{}'.format(instance.pk, filename.split('.')[-1]))


def move_deleted_image_to_new_path(image):
    old_path = image.imageUrl.__str__()
    today_date = datetime.date.today()
    new_path = 'image_delete/{}/{}/{}/{}.{}'.format(today_date.year, today_date.month, today_date.day, image.id,
                                                    old_path.split('.')[-1])
    if os.path.exists(old_path):
        try:
            os.rename(image.imageUrl.__str__(), new_path)
        except:
            os.makedirs(os.path.dirname(new_path))
            os.rename(image.imageUrl.__str__(), new_path)


def check_if_is_valid_save_and_return(serializer, serializer_detail=None, is_creation=False):
    if serializer.is_valid():
        object_for_serializer_detail = serializer.save()

        if is_creation:
            return Response({
                "status": "success",
                "data": serializer_detail(object_for_serializer_detail).data if serializer_detail else serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "success",
            "data": serializer_detail(object_for_serializer_detail).data if serializer_detail else serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        "status": "error",
        "data": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


def attempt_json_deserialize(data, expect_type=None):
    try:
        data = json.loads(data)
    except (TypeError, json.decoder.JSONDecodeError):
        pass

    if expect_type is not None and not isinstance(data, expect_type):
        raise ValueError(f"Got {type(data)} but expected {expect_type}.")

    return data
