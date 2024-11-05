import copy
import uuid

from django.core.exceptions import ValidationError
from django.db import models


class NavigationItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ForeignKey(
        'BackendTennis.Image',
        on_delete=models.SET_NULL,
        related_name='navigation_items',
        blank=True,
        null=True
    )
    route = models.ForeignKey(
        'BackendTennis.Route',
        on_delete=models.SET_NULL,
        related_name='navigation_items',
        blank=True,
        null=True
    )
    navBarRender = models.ForeignKey(
        'BackendTennis.Render',
        on_delete=models.SET_NULL,
        related_name='navigation_items',
        blank=True,
        null=True
    )
    pageRenders = models.ManyToManyField(
        'BackendTennis.PageRender',
        related_name='navigation_items'
    )

    childrenNavigationItems = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='parent_navigation_items'
    )

    enabled = models.BooleanField(default=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'route': self.route,
            'navBarRender': self.navBarRender,
            'pageRenders': self.pageRenders,
            'childrenNavigationItems': self.childrenNavigationItems,
            'enabled': self.enabled,
            'createAt': self.createAt,
            'updateAt': self.updateAt
        }
        return '%s' % to_return

    class Meta:
        app_label = 'BackendTennis'

    def _clean(self, instance: 'NavigationItem'):
        if self.navBarRender:
            if not self.parent_navigation_items.exists():
                self._validate_order_for_root_items(instance)
            else:
                self._validate_order_for_child_items(instance)
        self._validate_order_for_children_navigation_item(instance)

    @staticmethod
    def _validate_order_for_root_items(instance: 'NavigationItem'):
        """Valide l'ordre pour les items racine (sans parent)."""
        if NavigationItem.objects.filter(
                parent_navigation_items=None,
                navBarRender__order=instance.navBarRender.order
        ).exclude(id=instance.id).exists():
            raise ValidationError({
                'navBarRender': f'(root_items) Several elements use the same order'
                                f' [{instance.navBarRender.order}] for navBarRender'
            })

    @staticmethod
    def _validate_order_for_child_items(instance: 'NavigationItem'):
        """Valide l'ordre pour les items avec un parent."""
        for parent in instance.parent_navigation_items.all():
            if NavigationItem.objects.filter(
                    parent_navigation_items=parent,
                    navBarRender__order=instance.navBarRender.order
            ).exclude(id=instance.id).exists():
                raise ValidationError({
                    'navBarRender': f'(child_items) Several elements use the same order'
                                    f' [{instance.navBarRender.order}] for navBarRender'
                })

    @staticmethod
    def _validate_order_for_children_navigation_item(instance: 'NavigationItem'):
        """Valide les enfants de chaque item pour détecter les conflits d'ordre."""

        new_children_by_orders = {}

        for child in instance.childrenNavigationItems.all():
            if child.navBarRender is None:
                continue
            order = child.navBarRender.order
            if order not in new_children_by_orders:
                new_children_by_orders[order] = []
            new_children_by_orders[order].append(child.id)
        error_messages = []
        for order, children_with_same_order in new_children_by_orders.items():
            if len(children_with_same_order) > 1:
                error_messages.append(
                    f'(childrenNavigationItems) Several elements use the same order'
                    f' [{order}] for navBarRender of childrenNavigationItems'
                )
        if error_messages:
            raise ValidationError(
                {'childrenNavigationItems': '\n'.join(error_messages)}
            )

    def save(self, *args, **kwargs):
        instance_copy = copy.deepcopy(self)
        for attr, value in kwargs.items():
            match attr:
                case 'childrenNavigationItems':
                    instance_copy.childrenNavigationItems.set(value)
                case 'pageRenders':
                    instance_copy.pageRenders.set(value)
                case _:
                    setattr(instance_copy, attr, value)

        for attr in ['childrenNavigationItems', 'navBarRender']:
            if attr in kwargs:
                kwargs.pop(attr)

        self.full_clean()
        self._clean(instance_copy)
        super().save(*args, **kwargs)
