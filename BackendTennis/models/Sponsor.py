from django.db import models

from BackendTennis.models import Image
from BackendTennis.utils import create_id


class Sponsor(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default=create_id, editable=False)
    brandName = models.CharField(max_length=100, blank=False, null=True)
    image = models.ForeignKey(
        "BackendTennis.Image",
        on_delete=models.SET_NULL,
        related_name="sponsors",
        null=True
    )
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        to_return = {
            "id"       : self.id,
            "brandName": self.brandName,
            "image"    : self.image,
            "createAt" : self.createAt,
            "updateAt" : self.updateAt
        }
        return "%s" % to_return
    
    class Meta:
        app_label = "BackendTennis"
