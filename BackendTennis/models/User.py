import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group
from phonenumber_field.modelfields import PhoneNumberField

from BackendTennis.models.UserManager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthdate = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField()
    postal_code = models.CharField(max_length=10, validators=[
        RegexValidator(regex=r'^\d{5}$', message="Le code postal doit être composé de 5 chiffres.")])
    address = models.CharField(max_length=500)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    spouse = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='related_spouse_set')
    children = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='related_children_set')
    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', blank=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

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
