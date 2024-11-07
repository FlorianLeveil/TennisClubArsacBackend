from __future__ import annotations

from typing import TYPE_CHECKING

import uuid

from django.core.exceptions import ValidationError
from django.db import models

if TYPE_CHECKING:
    from ..models import AboutPage



class Sponsor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brandName = models.CharField(max_length=100, blank=False, null=True)
    image = models.ForeignKey(
        'BackendTennis.Image',
        on_delete=models.SET_NULL,
        related_name='sponsors',
        null=True
    )
    order = models.IntegerField(default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            'id': self.id,
            'brandName': self.brandName,
            'image': self.image,
            'order': self.order,
            'createAt': self.createAt,
            'updateAt': self.updateAt
        }
        return '%s' % to_return

    class Meta:
        ordering = ['createAt']
        app_label = 'BackendTennis'

    def validate_unique_order(self, page: AboutPage) -> None:
        if page.sponsors.filter(order=self.order).exclude(id=self.id).exists():
            raise ValidationError(
                {
                    'order': f'Order [{self.order}] of sponsor [{self.brandName}] already used by another Sponsor'
                             f' in the about page "{page.clubTitle}" .'}
            )

    def clean(self):
        for about_page in self.about_pages.all():
            self.validate_unique_order(about_page)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
