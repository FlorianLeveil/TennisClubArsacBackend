from rest_framework import serializers
from BackendTennis.models import Image, Category, Event
from BackendTennis.serializers import ImageSerializer, CategorySerializer


class EventSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=250, required=True)
    description = serializers.CharField(max_length=2000, required=True)
    dateType = serializers.CharField(max_length=50, required=True)
    images = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    start = serializers.DateField()
    end = serializers.DateField()
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Event
        fields = "__all__"
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        event = Event.objects.create(**validated_data)
        event.images.set(images_data)
        return event
    
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.dateType = validated_data.get('dateType', instance.dateType)
        images_data = validated_data.get('images', [])
        instance.images.set(images_data)
        instance.category = validated_data.get('category', instance.category)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.save()
        return instance


class EventDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    category = CategorySerializer()
    
    class Meta:
        model = Event
        fields = '__all__'
