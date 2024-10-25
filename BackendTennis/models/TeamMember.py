from django.db import models

from BackendTennis.models.base_model.BaseMember import BaseMember


class TeamMember(BaseMember):
    image = models.ForeignKey(
        'BackendTennis.Image',
        on_delete=models.SET_NULL,
        related_name='team_members',
        null=True
    )
    description = models.TextField()

    def __str__(self):
        to_return = {
            'id': self.id,
            'fullName': self.fullName,
            'role': self.role,
            'image': self.image,
            'description': self.description,
            'order': self.order,
            'createAt': self.createAt,
            'updateAt': self.updateAt,
        }
        return '%s' % to_return

    class Meta:
        ordering = ['order']
        app_label = 'BackendTennis'
