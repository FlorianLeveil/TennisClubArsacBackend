from rest_framework import serializers

from BackendTennis.models import MenuItemRow, Route
from BackendTennis.serializers import RouteSerializer


class MenuItemRowSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=100)
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all(), required=False)
    color = serializers.CharField(max_length=100, required=False)
    order = serializers.IntegerField(default=0, required=False)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = MenuItemRow
        fields = '__all__'

    @staticmethod
    def validate_order(value):
        if MenuItemRow.objects.filter(order=value).exists():
            raise serializers.ValidationError('Another MenuItemRow already use this order.')
        return value


class MenuItemRowDetailSerializer(serializers.ModelSerializer):
    route = RouteSerializer()

    class Meta:
        model = MenuItemRow
        fields = '__all__'
