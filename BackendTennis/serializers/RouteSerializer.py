from rest_framework import serializers

from BackendTennis.constant import constant_route_protocol_list
from BackendTennis.models import Route


class RouteSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100)
    protocol = serializers.ChoiceField(choices=constant_route_protocol_list)
    domainUrl = serializers.CharField(max_length=255)
    pathUrl = serializers.CharField(max_length=255, required=False)
    fullUrl = serializers.ReadOnlyField()
    componentPath = serializers.CharField(max_length=255, required=False)
    metaTitle = serializers.CharField(max_length=255, required=False)
    metaTags = serializers.JSONField(default=list, required=False)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Route
        fields = '__all__'

    @staticmethod
    def validate_domainUrl(value):
        if '/' in value:
            raise serializers.ValidationError('The \'domainUrl\' must not contain a path.')
        return value

    @staticmethod
    def validate_pathUrl(value):
        if value and not value.startswith('/'):
            raise serializers.ValidationError('The \'pathUrl\' must begin with \'/\'.')
        return value
