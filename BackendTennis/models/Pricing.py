from django.db import models
from BackendTennis.utils import create_id
from BackendTennis.validators import validate_pricing_type


class Pricing(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default=create_id, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    image = models.ForeignKey(
        "BackendTennis.Image",
        on_delete=models.SET_NULL,
        related_name="pricings",
        null=True
    )
    description = models.CharField(max_length=1000)
    price = models.FloatField(null=False)
    type = models.CharField(max_length=1000, validators=[validate_pricing_type])
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        to_return = {
            "id"         : self.id,
            "title"      : self.title,
            "image"      : self.image,
            "description": self.description,
            "price"      : self.price,
            "type"       : self.type,
            "createAt"   : self.createAt,
            "updateAt"   : self.updateAt
        }
        return "%s" % to_return
    
    class Meta:
        app_label = "BackendTennis"
