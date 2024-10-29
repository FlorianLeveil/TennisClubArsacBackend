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

    def create(self, validated_data):
        professors = validated_data.pop('professors', [])
        team_members = validated_data.pop('teamMembers', [])
        team_page = TeamPage.objects.create(**validated_data)
        team_page.professors.set(professors)
        team_page.teamMembers.set(team_members)
        return team_page

    def update(self, instance, validated_data):
        professors = validated_data.get('professors', None)
        if professors:
            instance.professors.set(professors)

        team_members = validated_data.get('teamMembers', None)
        if team_members:
            instance.teamMember.set(team_members)

        instance.professorsTitle = validated_data.get('professorsTitle', instance.professorsTitle)
        instance.professorsDescription = validated_data.get('professorsDescription', instance.professorsDescription)
        instance.teamMembersTitle = validated_data.get('teamMembersTitle', instance.teamMembersTitle)
        instance.dataCounter = validated_data.get('dataCounter', instance.dataCounter)
        instance.save()
        return instance


class TeamPageDetailSerializer(serializers.ModelSerializer):
    professors = ProfessorDetailSerializer(many=True)
    teamMembers = TeamMemberDetailSerializer(many=True)

    class Meta:
        model = TeamPage
        fields = '__all__'
