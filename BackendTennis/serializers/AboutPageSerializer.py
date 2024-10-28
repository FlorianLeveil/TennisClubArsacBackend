from rest_framework import serializers

from BackendTennis.constant import Constant
from BackendTennis.models import Image, ClubValue, Sponsor, AboutPage
from BackendTennis.serializers import ImageDetailSerializer, \
    ClubValueSerializer, SponsorDetailSerializer


class AboutPageSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    clubTitle = serializers.CharField(max_length=255, required=False)
    clubDescription = serializers.CharField(required=False)
    clubImage = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(),
        required=False
    )
    dataCounter = serializers.JSONField(default=list, required=False)
    clubValueTitle = serializers.CharField(max_length=255, required=False)
    clubValues = serializers.PrimaryKeyRelatedField(
        queryset=ClubValue.objects.all(),
        many=True,
        required=False
    )

    sponsorTitle = serializers.CharField(max_length=255, required=False)
    sponsors = serializers.PrimaryKeyRelatedField(
        queryset=Sponsor.objects.all(),
        many=True,
        required=False
    )

    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AboutPage
        fields = '__all__'

    @staticmethod
    def validate_clubImage(value):
        if value.type != Constant.IMAGE_TYPE.ABOUT_PAGE:
            raise serializers.ValidationError('Image must be of type \'about_page\'.')
        return value

    def create(self, validated_data):
        club_values = validated_data.pop('clubValues', [])
        sponsors = validated_data.pop('sponsors', [])

        about_page = AboutPage.objects.create(**validated_data)
        about_page.clubValues.set(club_values)
        about_page.sponsors.set(sponsors)
        return about_page

    def update(self, instance, validated_data):
        club_values = validated_data.get('clubValues', None)
        if club_values:
            instance.clubValues.set(club_values)

        sponsors = validated_data.get('sponsors', None)
        if sponsors:
            instance.sponsors.set(sponsors)

        instance.clubTitle = validated_data.get('clubTitle', instance.clubTitle)
        instance.clubDescription = validated_data.get('clubDescription', instance.clubDescription)
        instance.clubImage = validated_data.get('clubImage', instance.clubImage)
        instance.dataCounter = validated_data.get('dataCounter', instance.dataCounter)
        instance.clubValueTitle = validated_data.get('clubValueTitle', instance.clubValueTitle)
        instance.sponsorTitle = validated_data.get('sponsorTitle', instance.sponsorTitle)
        instance.save()
        return instance


class AboutPageDetailSerializer(serializers.ModelSerializer):
    clubImage = ImageDetailSerializer()
    clubValues = ClubValueSerializer(many=True)
    sponsors = SponsorDetailSerializer(many=True)

    class Meta:
        model = AboutPage
        fields = '__all__'
