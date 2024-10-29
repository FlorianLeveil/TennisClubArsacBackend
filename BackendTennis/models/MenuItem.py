import uuid

from django.db import models


class MenuItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    image = models.ForeignKey(
        'BackendTennis.Image',
        on_delete=models.SET_NULL,
        related_name='menu_items',
        null=True
    )
    route = models.ForeignKey(
        'BackendTennis.Route',
        on_delete=models.SET_NULL,
        related_name='menu_items',
        null=True
    )
    order = models.PositiveSmallIntegerField(default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'route': self.route,
            'rows': self.rows,
            'order': self.order,
            'createAt': self.createAt,
            'updateAt': self.updateAt
        }
        return '%s' % to_return

    class Meta:
        app_label = 'BackendTennis'
