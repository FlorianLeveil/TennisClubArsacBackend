import uuid

from django.core.validators import MinValueValidator
from django.db import models
from BackendTennis.validators import validate_pricing_type


class Pricing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    image = models.ForeignKey(
        "BackendTennis.Image",
        on_delete=models.SET_NULL,
        related_name="pricings",
        null=True
    )
    description = models.CharField(max_length=1000)
    price = models.FloatField(null=False, validators=[MinValueValidator(1)])
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
