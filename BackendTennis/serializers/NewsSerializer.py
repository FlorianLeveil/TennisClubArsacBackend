from rest_framework import serializers
from BackendTennis.models import Image, Category, News
from BackendTennis.serializers import CategorySerializer, ImageDetailSerializer


class NewsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=250, required=True)
    content = serializers.CharField(max_length=2000, required=True)
    subtitle = serializers.CharField(max_length=250, required=True)
    images = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = News
        fields = "__all__"
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        news = News.objects.create(**validated_data)
        news.images.set(images_data)
        return news
    
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.subtitle = validated_data.get('subtitle', instance.subtitle)
        images_data = validated_data.get('images', [])
        instance.images.set(images_data)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


class NewsDetailSerializer(serializers.ModelSerializer):
    images = ImageDetailSerializer(many=True)
    category = CategorySerializer()
    
    class Meta:
        model = News
        fields = '__all__'
