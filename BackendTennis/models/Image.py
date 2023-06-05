import uuid

from django.db import models
from BackendTennis.utils import compute_image_url
from BackendTennis.validators import validate_image_type


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    tags = models.ManyToManyField(
        "BackendTennis.Tag",
        related_name="images"
    )
    type = models.CharField(max_length=100, validators=[validate_image_type])
    imageUrl = models.ImageField(upload_to=compute_image_url, blank=True, null=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        to_return = {
            "id"      : self.id,
            "title"   : self.title,
            "tags"    : self.tags,
            "type"    : self.type,
            "imageUrl": self.imageUrl,
            "createAt": self.createAt,
            "updateAt": self.updateAt
        }
        return "%s" % to_return
    
    class Meta:
        app_label = "BackendTennis"
