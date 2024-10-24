from rest_framework import serializers

from BackendTennis.models import Professor


class BaseMemberSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    fullName = serializers.CharField(max_length=250, required=True)
    role = serializers.CharField(max_length=255)
    order = serializers.IntegerField(default=0)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        abstract = True
