import datetime
import json
import os
from pathlib import Path

from rest_framework import status
from rest_framework.response import Response

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DELETE_PATH = Path(PROJECT_ROOT, 'images_deleted')


def ensure_directory_exists(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def ensure_path_delete_exists():
    today = datetime.date.today()
    delete_path = Path(DELETE_PATH, str(today.year), str(today.month), str(today.day))
    ensure_directory_exists(delete_path)
    return delete_path


def compute_image_url(instance, filename):
    return os.path.join(instance.type, f'{instance.pk}.{filename.split('.')[-1]}')


def move_deleted_image_to_new_path(image):
    image_url = image.imageUrl.__str__()
    file_to_move = Path(PROJECT_ROOT, 'images', image.imageUrl.__str__())

    today = datetime.date.today()
    delete_path = Path(DELETE_PATH, str(today.year), str(today.month), str(today.day))
    ensure_directory_exists(delete_path)
    new_path = Path(delete_path, f'{image.id}.{image_url.split('.')[-1]}')

    if file_to_move.exists():
        file_to_move.rename(new_path)


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
