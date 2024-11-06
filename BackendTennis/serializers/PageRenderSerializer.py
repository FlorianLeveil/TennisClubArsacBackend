from rest_framework import serializers

from BackendTennis.constant import Constant
from BackendTennis.models import PageRender, Route, Render
from BackendTennis.serializers import RenderSerializer, RouteSerializer


class PageRenderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    render = serializers.PrimaryKeyRelatedField(queryset=Render.objects.all())
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PageRender
        fields = '__all__'

    @staticmethod
    def validate_render(render):
        if render.type in Constant.RENDER_TYPE_CHOICES.NAV_BAR:
            raise serializers.ValidationError('Render of PageRender cannot be of \'nav_bar\' type.')
        return render


class PageRenderDetailSerializer(serializers.ModelSerializer):
    route = RouteSerializer()
    render = RenderSerializer()

    class Meta:
        model = PageRender
        fields = '__all__'
