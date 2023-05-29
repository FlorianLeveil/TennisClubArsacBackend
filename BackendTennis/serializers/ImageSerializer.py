from rest_framework import serializers
from BackendTennis.models import Image


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=100, required=False)
    tags = serializers.ListField(required=False, child=serializers.CharField(max_length=100))
    type = serializers.ListField(required=False, child=serializers.CharField(max_length=100))
    imageUrl = serializers.ImageField(required=False)
    uploadedAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Image
        fields = "__all__"
    
    def create(self, validated_data):
        return Image.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance
