from rest_framework import serializers

from BackendTennis.models import Image, Pricing
from BackendTennis.serializers import ImageDetailSerializer
from BackendTennis.validators import validate_pricing_type


class PricingSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    license = serializers.BooleanField(required=True)
    siteAccess = serializers.BooleanField(required=True)
    extraData = serializers.JSONField()
    information = serializers.CharField(max_length=1000)
    price = serializers.FloatField(required=True)
    type = serializers.CharField(validators=[validate_pricing_type], required=True)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Pricing
        fields = "__all__"

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def create(self, validated_data):
        return Pricing.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.license = validated_data.get('license', instance.license)
        instance.siteAccess = validated_data.get('siteAccess', instance.siteAccess)
        instance.extraData = validated_data.get('extraData', instance.extraData)
        instance.information = validated_data.get('information', instance.information)
        instance.price = validated_data.get('price', instance.price)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance


class PricingDetailSerializer(serializers.ModelSerializer):
    image = ImageDetailSerializer()

    class Meta:
        model = Pricing
        fields = '__all__'
