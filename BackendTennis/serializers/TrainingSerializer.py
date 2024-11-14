from rest_framework import serializers

from BackendTennis.models import Training, User
from BackendTennis.serializers.UserSerializer import UserSerializer


class TrainingSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)
    unregisteredParticipants = serializers.ListField(child=serializers.CharField(max_length=255), default=list)
    cancel = serializers.BooleanField(default=False)
    start = serializers.DateTimeField(required=True)
    end = serializers.DateTimeField(required=True)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Training
        fields = "__all__"

    def validate(self, attrs):
        start = attrs.get('start', None)
        end = attrs.get('end', None)

        if start and end and start >= end:
            raise serializers.ValidationError("Start date must be before end date.")

        return attrs

    def create(self, validated_data):
        training_participants = validated_data.pop('participants', [])
        training = Training.objects.create(**validated_data)
        training.participants.set(training_participants)
        return training

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        participants_data = validated_data.get('participants', None)
        if participants_data:
            instance.participants.set(participants_data)
        instance.unregisteredParticipants = validated_data.get('unregisteredParticipants',
                                                               instance.unregisteredParticipants)
        instance.cancel = validated_data.get('cancel', instance.cancel)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.save()
        return instance


class TrainingDetailSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)

    class Meta:
        model = Training
        fields = '__all__'
