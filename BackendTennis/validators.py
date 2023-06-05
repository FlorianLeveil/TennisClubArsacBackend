from rest_framework.exceptions import ValidationError
from BackendTennis.constant import Constant

X = Constant

validated_image_type = [X.IMAGE_TYPE.PRICING, X.IMAGE_TYPE.NEWS, X.IMAGE_TYPE.EVENTS, X.IMAGE_TYPE.SPONSOR, X.IMAGE_TYPE.PICTURE]
validated_pricing_type = [X.PRICING_TYPE.OTHER, X.PRICING_TYPE.CHILDREN, X.PRICING_TYPE.ADULT]


def validate_type_for_str(validated_type, value):
    if value in validated_type:
        return value
    else:
        raise ValidationError("Bad Type. Type available : %s" % ', '.join(validated_type))


def validate_type_for_list(validated_type, value_list):
    if not all(value in validated_type for value in value_list):
        raise ValidationError("Bad Type. Type available : %s" % ', '.join(validated_type))
    else:
        return value_list
    
    
def validate_type(validated_type, value):
    value_type = type(value)
    if value_type == str:
        validate_type_for_str(validated_type, value)
    elif value_type == list:
        validate_type_for_list(validated_type, value)


def validate_pricing_type(value):
    validate_type(validated_pricing_type, value)


def validate_image_type(value):
    validate_type(validated_image_type, value)
