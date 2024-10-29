from rest_framework import serializers

from BackendTennis.constant import constant_nav_bar_position_list, constant_render_type_list
from BackendTennis.models import Render


class RenderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    order = serializers.IntegerField(default=0, required=False)
    navBarPosition = serializers.ChoiceField(choices=constant_nav_bar_position_list)
    visible = serializers.BooleanField(default=True, required=False)
    type = serializers.ChoiceField(choices=constant_render_type_list)
    color = serializers.CharField(max_length=30, required=False)
    isButton = serializers.BooleanField(default=False, required=False)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Render
        fields = '__all__'

    @staticmethod
    def validate_order(value):
        if Render.objects.filter(order=value).exists():
            raise serializers.ValidationError('Another Render already use this order.')
        return value
