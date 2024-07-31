from rest_framework import serializers
from BackendTennis.models import Tag


class TagSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=150)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Tag
        fields = "__all__"

    def validate_name(self, value):
        if value and not value[0].isdigit():
            return value[0].upper() + value[1:].lower()
        return value

    def create(self, validated_data):
        validated_data['name'] = self.validate_name(validated_data['name'])
        return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = self.validate_name(validated_data['name'])
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    def validate(self, data):
        """
        Ensure the name is unique.
        """
        if Tag.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError("Tag with this name already exists.")
        return data
