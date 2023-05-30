from rest_framework import serializers

from BackendTennis.models import Image, Pricing
from BackendTennis.serializers import ImageSerializer
from BackendTennis.validators import validate_pricing_type


class PricingSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    description = serializers.CharField(max_length=1000, required=True)
    price = serializers.FloatField(required=True)
    type = serializers.CharField(validators=[validate_pricing_type], required=True)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Pricing
        fields = "__all__"
    
    def create(self, validated_data):
        return Pricing.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance


class PricingDetailSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    
    class Meta:
        model = Pricing
        fields = '__all__'
