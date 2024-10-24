from rest_framework import serializers

from BackendTennis.constant import Constant
from BackendTennis.models import Image, TeamMember
from BackendTennis.serializers import ImageDetailSerializer


class TeamMemberSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    fullName = serializers.CharField(max_length=250, required=True)
    role = serializers.CharField(max_length=255)
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    description = serializers.CharField(max_length=10000)
    order = serializers.IntegerField(default=0)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TeamMember
        fields = "__all__"

    @staticmethod
    def validate_image(value):
        if value.type != Constant.IMAGE_TYPE.TEAM_MEMBER:
            raise serializers.ValidationError("Image must be of type 'team_member'.")
        return value

    def create(self, validated_data):
        return TeamMember.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.fullName = validated_data.get('fullName', instance.fullName)
        instance.role = validated_data.get('role', instance.role)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.order = validated_data.get('order', instance.order)
        instance.save()
        return instance


class TeamMemberDetailSerializer(serializers.ModelSerializer):
    image = ImageDetailSerializer()

    class Meta:
        model = TeamMember
        fields = '__all__'
