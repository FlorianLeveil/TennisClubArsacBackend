import uuid

from django.db import models

from BackendTennis.constant import constant_nav_bar_position_list, constant_render_type_list


class Render(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.IntegerField(default=0)
    navBarPosition = models.CharField(max_length=100, choices=constant_nav_bar_position_list)
    visible = models.BooleanField(default=True)
    type = models.CharField(max_length=100, choices=constant_render_type_list)
    color = models.CharField(max_length=30, null=True, blank=True)
    isButton = models.BooleanField(default=False)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            'id': self.id,
            'order': self.order,
            'navBarPosition': self.navBarPosition,
            'visible': self.visible,
            'type': self.type,
            'color': self.color,
            'isButton': self.isButton,
            'createAt': self.createAt,
            'updateAt': self.updateAt
        }
        return '%s' % to_return

    class Meta:
        app_label = 'BackendTennis'
