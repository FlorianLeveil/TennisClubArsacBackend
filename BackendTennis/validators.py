from rest_framework.exceptions import ValidationError


def validate_pricing_type(value):
    if value in ["other", "children", "adult"]:
        return value
    else:
        raise ValidationError("Bad Type. Type available : other, children, adult")