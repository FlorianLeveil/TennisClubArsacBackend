from rest_framework import serializers

from BackendTennis.constant import Constant
from BackendTennis.models import NavigationBar, NavigationItem, Route, Image
from BackendTennis.serializers import RouteSerializer, ImageDetailSerializer


class NavigationBarSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    logo = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), required=False)
    routeLogo = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all(), required=False)
    navigationItems = serializers.PrimaryKeyRelatedField(
        queryset=NavigationItem.objects.all(),
        many=True,
        required=False
    )
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = NavigationBar
        fields = '__all__'

    @staticmethod
    def validate_logo(value):
        if value.type != Constant.IMAGE_TYPE.NAVIGATION_BAR:
            raise serializers.ValidationError('Image must be of type \'navigation_bar\'.')
        return value


class NavigationBarDetailSerializer(serializers.ModelSerializer):
    logo = ImageDetailSerializer()
    routeLogo = RouteSerializer()

    class Meta:
        model = NavigationBar
        fields = '__all__'
