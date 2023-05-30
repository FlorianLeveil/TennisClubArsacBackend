from rest_framework import serializers
from BackendTennis.models import Image, Sponsor
from BackendTennis.serializers import ImageSerializer


class SponsorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    brandName = serializers.CharField(max_length=100, required=True)
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Sponsor
        fields = "__all__"
    
    def create(self, validated_data):
        return Sponsor.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.brandName = validated_data.get('brandName', instance.brandName)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class SponsorDetailSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    
    class Meta:
        model = Sponsor
        fields = '__all__'
