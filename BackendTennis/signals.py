import logging

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from BackendTennis.models import Render, NavigationItem

logger = logging.getLogger('BackendTennis.SIGNALS')


@receiver(pre_save, sender=Render)
def validate_navigation_items_on_render_update(sender, instance, **kwargs):
    logger.debug(f'[ {sender.__name__} ] Running update pre-saver asked by : {instance.id}')
    related_navigation_items = NavigationItem.objects.filter(navBarRender__id=instance.id)
    for nav_item in related_navigation_items:
        try:
            nav_item.save(navBarRender=instance)
        except ValidationError as e:
            raise e
