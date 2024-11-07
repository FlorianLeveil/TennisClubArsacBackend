import logging

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver

from BackendTennis.models import Render, NavigationItem, AboutPage, Sponsor

logger = logging.getLogger('BackendTennis.SIGNALS')


def _log_function_start_info(sender, instance):
    logger.debug(f'[ {sender.__name__} ] Running update pre-saver asked by : {instance.id}')


@receiver(pre_save, sender=Render)
def validate_navigation_items_on_render_update(sender, instance, **kwargs):
    _log_function_start_info(sender, instance)
    related_navigation_items = NavigationItem.objects.filter(navBarRender__id=instance.id)
    for nav_item in related_navigation_items:
        try:
            nav_item.save(navBarRender=instance)
        except ValidationError as e:
            raise e


@receiver(m2m_changed, sender=AboutPage.sponsors.through)
def validate_sponsor_order(sender, instance, action, **kwargs):
    _log_function_start_info(sender, instance)
    if action == 'pre_add':
        sponsor_ids = kwargs.get('pk_set', [])
        sponsors = Sponsor.objects.filter(id__in=sponsor_ids)
        for sponsor in sponsors:
            try:
                sponsor.validate_unique_order(instance)
            except ValidationError as e:
                raise e
