from rest_framework import serializers

from BackendTennis.models import PricingPage, Pricing
from BackendTennis.serializers import PricingDetailSerializer


class PricingPageSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False)
    pricing = serializers.PrimaryKeyRelatedField(
        queryset=Pricing.objects.all(),
        many=True,
        required=False
    )
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PricingPage
        fields = '__all__'


class PricingPageDetailSerializer(serializers.ModelSerializer):
    pricing = PricingDetailSerializer(many=True)

    class Meta:
        model = PricingPage
        fields = '__all__'
