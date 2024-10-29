import uuid

from django.db import models


class PageRender(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey(
        'BackendTennis.Route',
        on_delete=models.SET_NULL,
        related_name='page_renders',
        null=True
    )
    render = models.ForeignKey(
        'BackendTennis.Render',
        on_delete=models.CASCADE,
        related_name='page_renders',
    )
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            'id': self.id,
            'route': self.route,
            'render': self.render,
            'createAt': self.createAt,
            'updateAt': self.updateAt
        }
        return '%s' % to_return

    class Meta:
        app_label = 'BackendTennis'
