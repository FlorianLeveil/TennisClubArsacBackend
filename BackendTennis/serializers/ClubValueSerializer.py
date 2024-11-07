from rest_framework import serializers

from BackendTennis.models import ClubValue


class ClubValueSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    order = serializers.IntegerField(default=0)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ClubValue
        fields = '__all__'
