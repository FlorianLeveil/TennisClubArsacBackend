import uuid

from django.db import models

from BackendTennis.models import Pricing


class PricingPage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pricing = models.ManyToManyField(Pricing, related_name='pricing_pages')
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'pricing': self.pricing,
            'createAt': self.createAt,
            'updateAt': self.updateAt,
        }
        return '%s' % to_return

    class Meta:
        app_label = 'BackendTennis'
