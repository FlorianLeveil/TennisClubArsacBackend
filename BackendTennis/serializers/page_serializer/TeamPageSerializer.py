from rest_framework import serializers

from BackendTennis.models import TeamPage, Professor, TeamMember
from BackendTennis.serializers import ProfessorDetailSerializer, TeamMemberDetailSerializer


class TeamPageSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    professorsTitle = serializers.CharField(max_length=255, required=False)
    professorsDescription = serializers.CharField(required=False)
    professors = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all(), many=True, required=False)
    teamMembersTitle = serializers.CharField(max_length=255, required=False)
    teamMembers = serializers.PrimaryKeyRelatedField(queryset=TeamMember.objects.all(), many=True, required=False)
    dataCounter = serializers.JSONField(default=list, required=False)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TeamPage
        fields = '__all__'


class TeamPageDetailSerializer(serializers.ModelSerializer):
    professors = ProfessorDetailSerializer(many=True)
    teamMembers = TeamMemberDetailSerializer(many=True)

    class Meta:
        model = TeamPage
        fields = '__all__'
