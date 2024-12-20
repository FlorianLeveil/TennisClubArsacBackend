from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError

from BackendTennis.utils.string_utils import string_list_to_camel_case

if TYPE_CHECKING:
    from ..models import AboutPage, Sponsor, ClubValue, TeamPage

import logging

logger = logging.getLogger('BackendTennis.UniqueOrderValidationMixin')


class UniqueOrderValidationMixin:
    def validate_unique_order(self: Sponsor | ClubValue, page: AboutPage | TeamPage) -> None:
        """
        Validates that the unique order is valid.
        param: page: AboutPage
        """
        page_name_type = page._meta.verbose_name.capitalize()
        prop_name_in_page_model = string_list_to_camel_case(self._meta.verbose_name.split(' '))
        model_name = self._meta.object_name

        related_objects = getattr(page, prop_name_in_page_model + 's')
        if related_objects.filter(order=self.order).exclude(id=self.id).exists():
            error_message = (f'Order [{self.order}] of {model_name} [{self.id}] already used by another {model_name}'
                             f' in the {page_name_type} "{page.id}".')
            logger.error(error_message)
            raise ValidationError(
                {
                    'order': error_message
                }
            )
