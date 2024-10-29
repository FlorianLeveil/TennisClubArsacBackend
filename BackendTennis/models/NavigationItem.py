import uuid

from django.db import models


class NavigationItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    image = models.ForeignKey(
        'BackendTennis.Image',
        on_delete=models.SET_NULL,
        related_name='navigation_items',
        null=True
    )
    route = models.ForeignKey(
        'BackendTennis.Route',
        on_delete=models.SET_NULL,
        related_name='navigation_items',
        null=True
    )
    navBarRender = models.ForeignKey(
        'BackendTennis.Render',
        on_delete=models.SET_NULL,
        related_name='navigation_items',
        null=True
    )
    pageRenders = models.ManyToManyField(
        'BackendTennis.PageRender',
        related_name='navigation_items'
    )

    childrenNavigationItems = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='parent_navigation_items'
    )

    enabled = models.BooleanField(default=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'route': self.route,
            'navBarRender': self.navBarRender,
            'pageRenders': self.pageRenders,
            'childrenNavigationItems': self.childrenNavigationItems,
            'enabled': self.enabled,
            'createAt': self.createAt,
            'updateAt': self.updateAt
        }
        return '%s' % to_return

    class Meta:
        app_label = 'BackendTennis'
