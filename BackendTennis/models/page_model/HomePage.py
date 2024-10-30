import uuid

from django.db import models


class HomePage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, null=True, blank=True)
    navigationItems = models.ManyToManyField(
        'BackendTennis.NavigationItem',
        related_name='home_pages'
    )
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            'id': self.id,
            'title': self.title,
            'navigationItems': self.navigationItems,
            'createAt': self.createAt,
            'updateAt': self.updateAt,
        }
        return '%s' % to_return

    class Meta:
        app_label = 'BackendTennis'
