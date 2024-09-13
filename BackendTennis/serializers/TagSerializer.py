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
        value = ' '.join(value.split())

        if value[0].isdigit():
            parts = value.split(' ', 1)
            if len(parts) > 1:
                value = f"{parts[0]} {parts[1].capitalize()}"
            return value

        return value.capitalize()

    def validate(self, data):
        if Tag.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError("Tag with this name already exists.")
        return data

    def create(self, validated_data):
        validated_data['name'] = self.validate_name(validated_data['name'])
        return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = self.validate_name(validated_data['name'])

        if Tag.objects.exclude(id=instance.id).filter(name=validated_data['name']).exists():
            raise serializers.ValidationError("Tag with this name already exists.")

        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
