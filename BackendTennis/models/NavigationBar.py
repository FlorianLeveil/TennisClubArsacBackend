import uuid

from django.db import models


class NavigationBar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    logo = models.ForeignKey(
        'BackendTennis.Image',
        on_delete=models.SET_NULL,
        related_name='navigation_bars',
        null=True
    )
    routeLogo = models.ForeignKey(
        'BackendTennis.Route',
        on_delete=models.SET_NULL,
        related_name='navigation_bars',
        null=True
    )

    navigationItems = models.ManyToManyField(
        'BackendTennis.NavigationItem',
        related_name='navigation_bars'
    )

    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            'id': self.id,
            'logo': self.logo,
            'routeLogo': self.routeLogo,
            'navigationItems': self.navigationItems,
            'createAt': self.createAt,
            'updateAt': self.updateAt
        }
        return '%s' % to_return

    class Meta:
        app_label = 'BackendTennis'
