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
    price = models.FloatField(null=False, validators=[MinValueValidator(1)])
    license = models.BooleanField(null=False, default=False)
    site_access = models.BooleanField(null=False, default=False)
    extra_data = models.JSONField(null=False, blank=True, default=list)
    information = models.CharField(max_length=1000, blank=True, null=False)
    type = models.CharField(max_length=1000, validators=[validate_pricing_type])
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            "id": self.id,
            "title": self.title,
            "image": self.image,
            "license": self.license,
            "site_access": self.site_access,
            "extra_data": self.extra_data,
            "information": self.information,
            "price": self.price,
            "type": self.type,
            "createAt": self.createAt,
            "updateAt": self.updateAt
        }
        return "%s" % to_return

    class Meta:
        app_label = "BackendTennis"
