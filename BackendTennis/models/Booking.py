import uuid
from django.db import models


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clientFirstName = models.CharField(max_length=50)
    clientLastName = models.CharField(max_length=50)
    clientEmail = models.EmailField(max_length=100)
    clientPhoneNumber = models.CharField(max_length=30)
    payed = models.BooleanField(default=False)
    insurance = models.BooleanField(default=False)
    color = models.CharField(max_length=50, default="red")
    label = models.CharField(max_length=100, default="Réservé")
    start = models.DateField()
    end = models.DateField()
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        to_return = {
            "id"               : self.id,
            "clientFirstName"  : self.clientFirstName,
            "clientLastName"   : self.clientLastName,
            "clientEmail"      : self.clientEmail,
            "clientPhoneNumber": self.clientPhoneNumber,
            "payed"            : self.payed,
            "insurance"        : self.insurance,
            "color"            : self.insurance,
            "label"            : self.insurance,
            "start"            : self.start,
            "end"              : self.end,
            "createAt"         : str(self.createAt),
            "updateAt"         : str(self.updateAt)
        }
        return "%s" % to_return
    
    class Meta:
        app_label = "BackendTennis"
