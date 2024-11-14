from rest_framework import serializers

from BackendTennis.constant import Constant
from BackendTennis.models import Image, TeamMember
from BackendTennis.serializers import ImageDetailSerializer
from BackendTennis.serializers.base_serializer import BaseMemberSerializer


class TeamMemberSerializer(BaseMemberSerializer):
    fullNames = serializers.ListField(child=serializers.CharField(max_length=255), default=list)
    images = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True)
    description = serializers.CharField(max_length=10000)

    class Meta:
        model = TeamMember
        fields = '__all__'

    @staticmethod
    def validate_images(images):
        error_message = []
        for image in images:
            if image.type != Constant.IMAGE_TYPE.TEAM_MEMBER:
                error_message.append('Image must be of type \'team_member\'.')

        if error_message:
            raise serializers.ValidationError('\n'.join(error_message))
        return images


class TeamMemberDetailSerializer(serializers.ModelSerializer):
    images = ImageDetailSerializer(many=True)

    class Meta:
        model = TeamMember
        fields = '__all__'
