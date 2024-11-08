import uuid

from django.db import models

from ..mixins import UniqueOrderValidationMixin


class ClubValue(models.Model, UniqueOrderValidationMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'order': self.order,
            'createAt': self.createAt,
            'updateAt': self.updateAt
        }
        return '%s' % to_return

    class Meta:
        ordering = ['createAt']
        app_label = 'BackendTennis'

    def clean(self):
        for about_page in self.about_pages.all():
            self.validate_unique_order(about_page, self.title, about_page.clubTitle)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
