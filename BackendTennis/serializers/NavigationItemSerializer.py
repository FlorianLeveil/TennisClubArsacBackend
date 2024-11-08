from rest_framework import serializers

from BackendTennis.constant import Constant
from BackendTennis.models import NavigationItem, Route, Image, Render, PageRender
from BackendTennis.serializers import RouteSerializer, ImageDetailSerializer, RenderSerializer, \
    PageRenderDetailSerializer


class NavigationItemSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False)
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), required=False)

    navBarRender = serializers.PrimaryKeyRelatedField(queryset=Render.objects.all(), required=False)
    pageRenders = serializers.PrimaryKeyRelatedField(queryset=PageRender.objects.all(), many=True, required=False)
    childrenNavigationItems = serializers.PrimaryKeyRelatedField(
        queryset=NavigationItem.objects.all(),
        many=True,
        required=False
    )

    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all(), required=False)
    parent_navigation_items = serializers.SerializerMethodField(read_only=True)
    enabled = serializers.BooleanField(required=False)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = NavigationItem
        fields = '__all__'

    @staticmethod
    def get_parent_navigation_items(obj):
        parents = obj.parent_navigation_items.all()
        return NavigationItemSerializer(parents, many=True).data

    @staticmethod
    def validate_image(image):
        if image.type != Constant.IMAGE_TYPE.NAVIGATION_ITEM:
            raise serializers.ValidationError('Image must be of type \'navigation_item\'.')
        return image

    @staticmethod
    def validate_navBarRender(nav_bar_render):
        if nav_bar_render.type.lower() not in Constant.RENDER_TYPE_CHOICES.NAV_BAR:
            raise serializers.ValidationError('navBarRender must be of type \'nav_bar\'.')
        return nav_bar_render

    def update(self, instance, validated_data):
        if 'childrenNavigationItems' in validated_data:
            new_children_navigation_items = validated_data.pop('childrenNavigationItems', [])
            instance.save(childrenNavigationItems=new_children_navigation_items)
            instance.childrenNavigationItems.set(new_children_navigation_items)
        elif 'pageRenders' in validated_data:
            new_page_renders = validated_data.pop('pageRenders', [])
            instance.save(pageRenders=new_page_renders)
            instance.pageRenders.set(new_page_renders)
        else:
            instance.save()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        new_children_navigation_items = validated_data.pop('childrenNavigationItems', [])
        new_page_renders = validated_data.pop('pageRenders', [])
        instance = super().create(validated_data)
        instance.save(
            childrenNavigationItems=new_children_navigation_items,
            pageRenders=new_page_renders
        )
        instance.childrenNavigationItems.set(new_children_navigation_items)
        instance.pageRenders.set(new_page_renders)

        return instance


class NavigationItemDetailSerializer(serializers.ModelSerializer):
    image = ImageDetailSerializer()
    navBarRender = RenderSerializer()
    pageRenders = PageRenderDetailSerializer(many=True)
    childrenNavigationItems = serializers.SerializerMethodField()
    route = RouteSerializer()

    class Meta:
        model = NavigationItem
        fields = '__all__'

    @staticmethod
    def get_childrenNavigationItems(obj):
        children = obj.childrenNavigationItems.all()
        return NavigationItemDetailSerializer(children, many=True).data
