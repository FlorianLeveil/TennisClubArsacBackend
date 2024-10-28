import uuid

from django.db import models

from BackendTennis.constant import constant_route_protocol_list


class Route(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    protocol = models.CharField(max_length=100, choices=constant_route_protocol_list)
    domainUrl = models.CharField(max_length=255)
    pathUrl = models.CharField(max_length=255, null=True, blank=True)
    componentPath = models.CharField(max_length=255, null=True, blank=True)
    metaTitle = models.CharField(max_length=255, null=True, blank=True)
    metaTags = models.JSONField(default=list)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    @property
    def fullUrl(self):
        path = f'/{self.pathUrl.lstrip('/')}' if self.pathUrl else ''
        return f'{self.protocol}://{self.domainUrl}{path}'

    def __str__(self):
        to_return = {
            'id': self.id,
            'name': self.name,
            'protocol': self.protocol,
            'domainUrl': self.domainUrl,
            'pathUrl': self.pathUrl,
            'fullUrl': self.fullUrl,
            'componentPath': self.componentPath,
            'metaTitle': self.metaTitle,
            'metaTags': self.metaTags,
            'createAt': self.createAt,
            'updateAt': self.updateAt
        }
        return '%s' % to_return

    class Meta:
        app_label = 'BackendTennis'
