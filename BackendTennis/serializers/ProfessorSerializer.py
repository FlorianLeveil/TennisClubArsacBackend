from rest_framework import serializers

from BackendTennis.constant import Constant
from BackendTennis.models import Image, Professor
from BackendTennis.serializers import ImageDetailSerializer
from BackendTennis.serializers.base_serializer import BaseMemberSerializer


class ProfessorSerializer(BaseMemberSerializer):
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    diploma = serializers.CharField(max_length=1000)
    year_experience = serializers.CharField(max_length=25)
    best_rank = serializers.CharField(max_length=25)

    class Meta:
        model = Professor
        fields = '__all__'

    @staticmethod
    def validate_image(value):
        if value.type != Constant.IMAGE_TYPE.PROFESSOR:
            raise serializers.ValidationError('Image must be of type \'professor\'.')
        return value


class ProfessorDetailSerializer(serializers.ModelSerializer):
    image = ImageDetailSerializer()

    class Meta:
        model = Professor
        fields = '__all__'
