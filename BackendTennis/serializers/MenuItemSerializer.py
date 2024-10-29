from rest_framework import serializers

from BackendTennis.constant import Constant
from BackendTennis.models import MenuItem, Route, Image, MenuItemRow
from BackendTennis.serializers import RouteSerializer, ImageDetailSerializer, MenuItemRowDetailSerializer


class MenuItemSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False)
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), required=False)
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all(), required=False)
    rows = serializers.PrimaryKeyRelatedField(queryset=MenuItemRow.objects.all(), many=True, required=False)
    order = serializers.IntegerField(default=0, required=False)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = MenuItem
        fields = '__all__'

    @staticmethod
    def validate_image(value):
        if value.type != Constant.IMAGE_TYPE.MENU_ITEM:
            raise serializers.ValidationError('Image must be of type \'menuitem\'.')
        return value

    @staticmethod
    def validate_order(value):
        if MenuItem.objects.filter(order=value).exists():
            raise serializers.ValidationError('Another MenuItem already use this order.')
        return value


class MenuItemDetailSerializer(serializers.ModelSerializer):
    image = ImageDetailSerializer()
    route = RouteSerializer()
    rows = MenuItemRowDetailSerializer(many=True)

    class Meta:
        model = MenuItem
        fields = '__all__'
