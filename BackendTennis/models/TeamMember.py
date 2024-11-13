from django.contrib.postgres.fields import ArrayField
from django.db import models

from BackendTennis.mixins import UniqueOrderValidationMixin
from BackendTennis.models.base_model.BaseMember import BaseMember


class TeamMember(BaseMember, UniqueOrderValidationMixin):
    fullNames = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    images = models.ManyToManyField(
        'BackendTennis.Image',
        related_name='team_members'
    )
    description = models.TextField()

    def __str__(self):
        to_return = {
            'id': self.id,
            'fullNames': self.fullNames,
            'role': self.role,
            'images': self.images,
            'description': self.description,
            'order': self.order,
            'createAt': self.createAt,
            'updateAt': self.updateAt,
        }
        return '%s' % to_return

    class Meta:
        ordering = ['order']
        app_label = 'BackendTennis'

    def clean(self):
        for team_page in self.team_pages.all():
            self.validate_unique_order(team_page)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
