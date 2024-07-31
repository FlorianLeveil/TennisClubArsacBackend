from rest_framework import serializers
from BackendTennis.models import Event, Image, Category
from BackendTennis.serializers import ImageDetailSerializer, CategorySerializer


class EventSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=250, required=True)
    description = serializers.CharField(max_length=2000, required=True)
    dateType = serializers.CharField(max_length=50, required=True)
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Event
        fields = "__all__"

    def validate(self, attrs):
        if attrs['start'] >= attrs['end']:
            raise serializers.ValidationError("Start date must be before end date.")
        return attrs

    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        return event

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.dateType = validated_data.get('dateType', instance.dateType)
        instance.image = validated_data.get('image', instance.image)
        instance.category = validated_data.get('category', instance.category)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.save()
        return instance


class EventDetailSerializer(serializers.ModelSerializer):
    image = ImageDetailSerializer()
    category = CategorySerializer()

    class Meta:
        model = Event
        fields = '__all__'
