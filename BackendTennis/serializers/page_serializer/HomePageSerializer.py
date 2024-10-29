from rest_framework import serializers

from BackendTennis.models import NavigationItem, HomePage
from BackendTennis.serializers import NavigationItemDetailSerializer


class HomePageSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=100)
    menuItems = serializers.PrimaryKeyRelatedField(queryset=NavigationItem.objects.all(), many=True, required=False)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = HomePage
        fields = '__all__'


class HomePageDetailSerializer(serializers.ModelSerializer):
    menuItems = NavigationItemDetailSerializer(many=True)

    class Meta:
        model = HomePage
        fields = '__all__'
