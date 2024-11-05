from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from BackendTennis.models import NavigationItem


@transaction.atomic
def update_multiple_navigation_items(navigation_items_updates: list[dict]):
    """
    Multiple update of NavigationItem objects with a transaction.

    :param navigation_items_updates: list[dict]
    """
    for update_data in navigation_items_updates:
        try:
            nav_item = NavigationItem.objects.get(id=update_data['id'])
        except ObjectDoesNotExist:
            raise ValueError(f'NavigationItem with ID {update_data['id']} not found.')

        update_data.pop('id', None)

        nav_item.save(**update_data)
