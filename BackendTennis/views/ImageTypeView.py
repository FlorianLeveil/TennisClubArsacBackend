from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from BackendTennis.authentication import CustomAPIKeyAuthentication
from BackendTennis.constant import Constant


class ImageTypeListView(APIView):
    authentication_classes = [CustomAPIKeyAuthentication, JWTAuthentication]
    permission_classes = [AllowAny]

    @extend_schema(
        summary='Get list of image types',
        responses={200: dict},
        tags=['ImageTypes']
    )
    def get(self, request, *args, **kwargs):
        types_with_labels = [
            {
                'key': value['key'],
                'label': value['label']
            }
            for value in vars(Constant.IMAGE_TYPE_TRAD).values()
        ]
        return Response({'types': types_with_labels})
