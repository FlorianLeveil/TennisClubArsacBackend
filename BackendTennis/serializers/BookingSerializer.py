from django.utils import timezone
from rest_framework import serializers

from BackendTennis.models import Booking
from BackendTennis.utils import create_id


class BookingSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    clientFirstName = serializers.CharField(max_length=50, required=True)
    clientLastName = serializers.CharField(max_length=50, required=True)
    clientEmail = serializers.EmailField(max_length=100, required=True)
    clientPhoneNumber = serializers.CharField(required=True)
    payed = serializers.BooleanField(required=False)
    insurance = serializers.BooleanField(required=False)
    color = serializers.CharField(max_length=50, required=True)
    label = serializers.CharField(max_length=100, required=True)
    start = serializers.DateField(required=True)
    end = serializers.DateField(required=True)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"

    def create(self, validated_data):
        validated_data["id"] = create_id()
        return Booking.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.clientFirstName = validated_data.get('clientFirstName', instance.clientFirstName)
        instance.clientLastName = validated_data.get('clientLastName', instance.clientLastName)
        instance.clientEmail = validated_data.get('clientEmail', instance.clientEmail)
        instance.clientPhoneNumber = validated_data.get('clientPhoneNumber', instance.clientPhoneNumber)
        instance.payed = validated_data.get('payed', instance.payed)
        instance.insurance = validated_data.get('insurance', instance.insurance)
        instance.color = validated_data.get('color', instance.clientLastName)
        instance.label = validated_data.get('label', instance.clientLastName)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.save()
        return instance