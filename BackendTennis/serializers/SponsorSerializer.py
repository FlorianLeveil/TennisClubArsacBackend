from rest_framework import serializers

from BackendTennis.constant import Constant
from BackendTennis.models import Image, Sponsor
from BackendTennis.serializers import ImageDetailSerializer


class SponsorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    brandName = serializers.CharField(max_length=100, required=True)
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    order = serializers.IntegerField(default=0, required=False)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Sponsor
        fields = '__all__'

    @staticmethod
    def validate_image(value):
        if value.type != Constant.IMAGE_TYPE.SPONSOR:
            raise serializers.ValidationError('Image must be of type \'sponsor\'.')
        return value


class SponsorDetailSerializer(serializers.ModelSerializer):
    image = ImageDetailSerializer()

    class Meta:
        model = Sponsor
        fields = '__all__'
