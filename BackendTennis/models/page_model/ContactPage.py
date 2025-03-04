import uuid

from django.db import models


class ContactPage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    mapAddress = models.TextField(null=True, blank=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            'id': self.id,
            'description': self.description,
            'mapAddress': self.mapAddress,
            'createAt': self.createAt,
            'updateAt': self.updateAt,
        }
        return '%s' % to_return

    class Meta:
        app_label = 'BackendTennis'
