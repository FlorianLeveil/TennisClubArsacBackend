from rest_framework.exceptions import ValidationError
from BackendTennis.constant import Constant

X = Constant


def validate_type(validated_type, value):
    if value in validated_type:
        return value
    else:
        raise ValidationError("Bad Type. Type available : %s" % ', '.join(validated_type))


def validate_pricing_type(value):
    validated_type = [X.PRICING_TYPE.OTHER, X.PRICING_TYPE.CHILDREN, X.PRICING_TYPE.ADULT]
    validate_type(validated_type, value)


def validate_image_type(value):
    validated_type = [X.IMAGE_TYPE.PRICING, X.IMAGE_TYPE.NEWS, X.IMAGE_TYPE.EVENTS, X.IMAGE_TYPE.SPONSOR, X.IMAGE_TYPE.PICTURE]
    validate_type(validated_type, value)
