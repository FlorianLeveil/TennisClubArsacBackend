import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthdate = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField()
    postal_code = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^\d{5}$', message="Le code postal doit être composé de 5 chiffres.")])
    address = models.CharField(max_length=500)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    spouse = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    children = models.ManyToManyField('self', symmetrical=False, blank=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthdate": self.birthdate,
            "email": self.email,
            "phone_number": self.phone_number,
            "postal_code": self.postal_code,
            "address": self.address,
            "street": self.street,
            "city": self.city,
            "country": self.country,
            "spouse": str(self.spouse) if self.spouse else None,
            "children": [str(child) for child in self.children.all()],
            "createAt": str(self.createAt),
            "updateAt": str(self.updateAt)
        }
        return "%s" % to_return

    class Meta:
        app_label = "BackendTennis"
