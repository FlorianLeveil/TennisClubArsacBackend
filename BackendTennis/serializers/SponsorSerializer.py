from django.utils import timezone
from rest_framework import serializers

from BackendTennis.models import Image, Sponsor
from BackendTennis.serializers import ImageSerializer
from BackendTennis.utils import create_id, attempt_json_deserialize


class SponsorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    brandName = serializers.CharField(max_length=100, required=True)
    image = serializers.PrimaryKeyRelatedField(read_only=True)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Sponsor
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        image_pk = validated_data['image_id']
        image_pk = attempt_json_deserialize(image_pk, expect_type=str)
        instance = super().create(validated_data)
        return instance
        # return Sponsor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.brandName = validated_data.get('title', instance.title)
        image_data = self.context['request'].data.get('image')
        image_data = attempt_json_deserialize(image_data, expect_type=str)
        validated_data['image_id'] = image_data
        return instance
