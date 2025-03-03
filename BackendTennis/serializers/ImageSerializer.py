from rest_framework import serializers

from BackendTennis.models import Image, Tag
from BackendTennis.serializers import TagSerializer
from BackendTennis.validators import validate_image_type


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    type = serializers.CharField(max_length=100, validators=[validate_image_type], required=True)
    imageUrl = serializers.ImageField(required=True)
    imageUrlLink = serializers.SerializerMethodField(read_only=True)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Image
        fields = "__all__"

    @staticmethod
    def get_imageUrlLink(obj):
        if obj.imageUrl:
            return obj.imageUrl.url
        return None

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        image = Image.objects.create(**validated_data)
        image.tags.set(tags_data)
        return image

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        tags_data = validated_data.get('tags', None)
        if tags_data:
            instance.tags.set(tags_data)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance


class ImageDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Image
        fields = '__all__'
