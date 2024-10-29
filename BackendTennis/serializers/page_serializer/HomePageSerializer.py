from rest_framework import serializers

from BackendTennis.models import MenuItem, HomePage
from BackendTennis.serializers import MenuItemDetailSerializer


class HomePageSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=100)
    menuItems = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(), many=True, required=False)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = HomePage
        fields = '__all__'


class HomePageDetailSerializer(serializers.ModelSerializer):
    menuItems = MenuItemDetailSerializer(many=True)

    class Meta:
        model = HomePage
        fields = '__all__'
