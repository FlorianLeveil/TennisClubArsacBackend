from rest_framework import serializers
from BackendTennis.models import Category


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100, required=False)
    icon = serializers.CharField(max_length=1000, required=False)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Category
        fields = "__all__"
    
    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.save()
        return instance
