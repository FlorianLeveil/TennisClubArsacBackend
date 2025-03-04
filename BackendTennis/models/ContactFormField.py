import uuid

from django.db import models

from BackendTennis.constant import constant_form_input_name
from BackendTennis.models.page_model.ContactPage import ContactPage


class ContactFormField(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.ForeignKey(ContactPage, on_delete=models.CASCADE, related_name='form_fields')
    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=constant_form_input_name)
    max_length = models.IntegerField(null=True, blank=True)
    required = models.BooleanField(default=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            'id': self.id,
            'page': self.page,
            'label': self.label,
            'field_type': self.field_type,
            'max_length': self.max_length,
            'required': self.required,
            'createAt': self.createAt,
            'updateAt': self.updateAt,
        }
        return '%s' % to_return

    class Meta:
        app_label = 'BackendTennis'
