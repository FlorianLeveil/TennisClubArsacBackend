from rest_framework import serializers

from BackendTennis.constant import Constant
from BackendTennis.models import Image, Professor
from BackendTennis.serializers import ImageDetailSerializer
from BackendTennis.serializers.base_serializer import BaseMemberSerializer


class ProfessorSerializer(BaseMemberSerializer):
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    diploma = serializers.CharField(max_length=1000)
    year_experience = serializers.IntegerField(default=0)
    best_rank = serializers.CharField(max_length=25)

    class Meta:
        model = Professor
        fields = '__all__'

    @staticmethod
    def validate_image(value):
        if value.type != Constant.IMAGE_TYPE.PROFESSOR:
            raise serializers.ValidationError('Image must be of type \'professor\'.')
        return value

    @staticmethod
    def validate_order(value):
        if Professor.objects.filter(order=value).exists():
            raise serializers.ValidationError('Another Professor already use this order.')
        return value

    def create(self, validated_data):
        return Professor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.fullName = validated_data.get('fullName', instance.fullName)
        instance.role = validated_data.get('role', instance.role)
        instance.order = validated_data.get('order', instance.order)

        instance.image = validated_data.get('image', instance.image)
        instance.diploma = validated_data.get('diploma', instance.diploma)
        instance.year_experience = validated_data.get('year_experience', instance.year_experience)
        instance.best_rank = validated_data.get('best_rank', instance.best_rank)
        instance.save()
        return instance


class ProfessorDetailSerializer(serializers.ModelSerializer):
    image = ImageDetailSerializer()

    class Meta:
        model = Professor
        fields = '__all__'
