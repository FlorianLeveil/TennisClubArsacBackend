import uuid

from django.db import models


class TeamMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullName = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=255)
    image = models.ForeignKey(
        'BackendTennis.Image',
        on_delete=models.SET_NULL,
        related_name='team_members',
        null=True
    )
    description = models.CharField(max_length=10000)
    order = models.PositiveSmallIntegerField(default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

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
