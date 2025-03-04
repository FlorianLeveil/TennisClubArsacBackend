import uuid
from django.db import models


class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250, blank=False, null=False)
    content = models.CharField(max_length=2000, blank=False, null=False)
    subtitle = models.CharField(max_length=250, blank=False, null=False)
    images = models.ManyToManyField(
        "BackendTennis.Image",
        related_name="newss"
    )
    category = models.ForeignKey(
        "BackendTennis.Category",
        on_delete=models.SET_NULL,
        related_name="newss",
        null=True
    )
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "subtitle": self.subtitle,
            "images": self.images,
            "category": self.category,
            "createAt": self.createAt,
            "updateAt": self.updateAt
        }
        return "%s" % to_return

    class Meta:
        app_label = "BackendTennis"
