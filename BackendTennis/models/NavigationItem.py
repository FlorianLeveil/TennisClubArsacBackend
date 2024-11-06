from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import models

if TYPE_CHECKING:
    from ..models import Render, PageRender
    from typing import Dict

logger = logging.getLogger(__name__)


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

    def _clean(self):
        if self.navBarRender:
            if not self.parent_navigation_items.exists():
                self._validate_navBarRender_order_for_root_items()
            else:
                self._validate_navBarRender_order_for_child_items()
        self._validate_navBarRender_order_for_children_navigation_item()

        if self.pageRenders:
            self._validate_same_type_page_renders()
            if not self.parent_navigation_items.exists():
                self._validate_pageRenders_order_for_root_items()
            else:
                self._validate_pageRenders_order_for_child_items()
            self._validate_pageRender_order_for_children_navigation_item()

    def _validate_navBarRender_order_for_root_items(self):
        """Validate the order for root items (without a parent)."""
        if NavigationItem.objects.filter(
                parent_navigation_items=None,
                navBarRender__order=self.navBarRender.order,
                navBarRender__navBarPosition=self.navBarRender.navBarPosition
        ).exclude(id=self.id).exists():
            logger.debug(f'(root_items) [{self.id}] Several elements use the same order [{self.navBarRender.order}] '
                         f'for navBarRender')
            raise ValidationError({
                'navBarRender': f'(root_items) Several elements use the same order'
                                f' [{self.navBarRender.order}] for navBarRender'
            })

    def _validate_pageRenders_order_for_root_items(self):
        """Validate the pageRenders order for root items (without a parent)."""
        for page_render in self.pageRenders.all():
            if NavigationItem.objects.filter(
                    parent_navigation_items=None,
                    pageRenders__render__type=page_render.render.type,
                    pageRenders__render__order=page_render.render.order
            ).exclude(id=self.id).exists():
                raise ValidationError({
                    'pageRenders': f'(root_items) Several elements use the same order'
                                   f' [{page_render.render.order}] for pageRenders of type [{page_render.render.type}]'
                })

    def _validate_navBarRender_order_for_child_items(self):
        """Validate the order for items with a parent."""
        for parent in self.parent_navigation_items.all():
            if NavigationItem.objects.filter(
                    parent_navigation_items=parent,
                    navBarRender__order=self.navBarRender.order,
                    navBarRender__navBarPosition=self.navBarRender.navBarPosition
            ).exclude(id=self.id).exists():
                logger.debug(
                    f'(root_items) [{self.id}] Several elements use the same order [{self.navBarRender.order}] '
                    f'for navBarRender')
                raise ValidationError({
                    'navBarRender': f'(child_items) Several elements use the same order'
                                    f' [{self.navBarRender.order}] for navBarRender'
                })

    def _validate_pageRenders_order_for_child_items(self):
        """Validate the order for items with a parent."""
        for parent in self.parent_navigation_items.all():
            for page_render in self.pageRenders.all():
                if NavigationItem.objects.filter(
                        parent_navigation_items=parent,
                        pageRenders__render__type=page_render.render.type,
                        pageRenders__render__order=page_render.render.order
                ).exclude(id=self.id).exists():
                    raise ValidationError({
                        'pageRenders': f'(child_items) Several elements use the same order'
                                       f' [{page_render.render.order}] for pageRenders of type [{page_render.render.type}]'
                                       f' for parent [{parent.title}]'
                    })

    def _validate_order_for_children_navigation_item(
            self,
            prop_name: str,
            prop_value: Render | PageRender,
            child_title: str,
            order: int,
            children_orders_by: Dict,
            error_message_template: callable
    ) -> None:
        """Validate each item's children to detect order conflicts."""
        if prop_name == 'childrenNavigationItems':
            ordered_by_value = prop_value.navBarPosition
        else:
            ordered_by_value = prop_value.render.type

        if ordered_by_value not in children_orders_by:
            children_orders_by[ordered_by_value] = {}

        children_by_order = children_orders_by[ordered_by_value]
        if order not in children_by_order:
            children_by_order[order] = []
        children_by_order[order].append(child_title)

        error_messages = []
        for ordered_by_value, children_by_order in children_orders_by.items():
            for order, children_with_same_order in children_by_order.items():
                if len(children_with_same_order) > 1:
                    error_messages.append(
                        error_message_template(prop_name, order, ordered_by_value, self.title, children_with_same_order)
                    )
        if error_messages:
            logger.debug('\n'.join(error_messages))
            raise ValidationError(
                {'childrenNavigationItems': '\n'.join(error_messages)}
            )

    @staticmethod
    def _get_validation_for_children_error_message_template(prop_name: str) -> callable:
        if prop_name == 'childrenNavigationItems':
            return (lambda _prop_name, order, ordered_by_value, parent_title, children_with_same_order:
                    f'({_prop_name}) Several elements use the same order [{order}] and position [{ordered_by_value}]'
                    f' for navBarRender of {_prop_name} for parent [{parent_title}] :'
                    f' [{', '.join(children_with_same_order)}]')
        else:
            return (
                lambda _prop_name, order, ordered_by_value, parent_title, children_with_same_order:
                f'({_prop_name}) Several elements use the same order'
                f' [{order}] for pageRenders of type [{ordered_by_value}]'
                f' for parent [{parent_title}] : [{', '.join(children_with_same_order)}]'
            )

    def _validate_navBarRender_order_for_children_navigation_item(self):
        children_orders_by = {}
        prop_name = 'childrenNavigationItems'
        error_message_template = self._get_validation_for_children_error_message_template(prop_name)
        for child in self.childrenNavigationItems.all():
            if child.navBarRender is None:
                continue
            self._validate_order_for_children_navigation_item(
                prop_name,
                child.navBarRender,
                child.title,
                child.navBarRender.order,
                children_orders_by,
                error_message_template
            )

    def _validate_pageRender_order_for_children_navigation_item(self):
        """Validate each item's children to detect order conflicts."""
        children_orders_by = {}
        prop_name = 'pageRenders'
        error_message_template = self._get_validation_for_children_error_message_template(prop_name)
        for child in self.childrenNavigationItems.all():
            if child.pageRenders is None:
                continue
            for page_render in child.pageRenders.all():
                self._validate_order_for_children_navigation_item(
                    prop_name,
                    page_render,
                    child.title,
                    page_render.render.order,
                    children_orders_by,
                    error_message_template
                )

    def _validate_same_type_page_renders(self):
        """Validate the order for page renders."""
        page_renders_id_by_type = {}
        for page in self.pageRenders.all():
            page_type = page.render.type
            if page_type not in page_renders_id_by_type:
                page_renders_id_by_type[page_type] = []
            page_renders_id_by_type[page_type].append(str(page.id))
        error_messages = []
        for page_type, pages_id in page_renders_id_by_type.items():
            if len(pages_id) > 1:
                error_messages.append(
                    f'Too many PageRender with same type [{page_type}] : [{', '.join(pages_id)}]'
                )
        if error_messages:
            raise ValidationError(
                {'pageRenders': '\n'.join(error_messages)}
            )

    def save(self, *args, **kwargs):
        for attr, value in kwargs.items():
            match attr:
                case 'childrenNavigationItems':
                    self.childrenNavigationItems.set(value)
                case 'pageRenders':
                    self.pageRenders.set(value)
                case _:
                    setattr(self, attr, value)

        for attr in ['title', 'description', 'image', 'route', 'navBarRender',
                     'pageRenders', 'childrenNavigationItems', 'enabled']:
            if attr in kwargs:
                kwargs.pop(attr)

        self.full_clean()
        self._clean()
        super().save(*args, **kwargs)
