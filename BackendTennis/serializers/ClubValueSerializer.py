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

    @staticmethod
    def validate_order(value):
        if ClubValue.objects.filter(order=value).exists():
            raise serializers.ValidationError('Another Club Value already use this order.')
        return value

    def create(self, validated_data):
        return ClubValue.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.order = validated_data.get('order', instance.order)
        instance.save()
        return instance
