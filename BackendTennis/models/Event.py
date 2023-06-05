import uuid
from django.db import models


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=2000, blank=False, null=False)
    dateType = models.CharField(max_length=50, blank=False, null=False)
    start = models.DateField()
    end = models.DateField()
    image = models.ForeignKey(
        "BackendTennis.Image",
        on_delete=models.SET_NULL,
        related_name="events",
        null=True
    )
    category = models.ForeignKey(
        "BackendTennis.Category",
        on_delete=models.SET_NULL,
        related_name="events",
        null=True
    )
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        to_return = {
            "id"         : self.id,
            "title"      : self.title,
            "description": self.description,
            "dateType"   : self.dateType,
            "start"      : self.start,
            "end"        : self.end,
            "image"      : self.image,
            "category"   : self.category,
            "createAt"   : self.createAt,
            "updateAt"   : self.updateAt
        }
        return "%s" % to_return
    
    class Meta:
        app_label = "BackendTennis"
