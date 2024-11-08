from rest_framework import serializers

from BackendTennis.constant import Constant
from BackendTennis.models import Image, TeamMember
from BackendTennis.serializers import ImageDetailSerializer
from BackendTennis.serializers.base_serializer import BaseMemberSerializer


class TeamMemberSerializer(BaseMemberSerializer):
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    description = serializers.CharField(max_length=10000)

    class Meta:
        model = TeamMember
        fields = '__all__'

    @staticmethod
    def validate_image(value):
        if value.type != Constant.IMAGE_TYPE.TEAM_MEMBER:
            raise serializers.ValidationError('Image must be of type \'team_member\'.')
        return value


class TeamMemberDetailSerializer(serializers.ModelSerializer):
    image = ImageDetailSerializer()

    class Meta:
        model = TeamMember
        fields = '__all__'
