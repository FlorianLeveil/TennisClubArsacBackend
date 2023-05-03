import time
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from BackendTennis.utils import create_id, compute_image_url


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    tags = ArrayField(models.CharField(max_length=100), default=list)
    type = ArrayField(models.CharField(max_length=100))
    imageUrl = models.ImageField(upload_to=compute_image_url, blank=True, null=True)
    uploadedAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            "id": self.id,
            "title": self.title,
            "tags": self.tags,
            "type": self.type,
            "imageUrl": self.imageUrl,
            "uploadedAt": self.uploadedAt,
            "updateAt": self.updateAt
        }
        return "%s" % to_return

    class Meta:
        app_label = "BackendTennis"
