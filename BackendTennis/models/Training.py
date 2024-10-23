import uuid

from django.contrib.postgres import fields
from django.db import models


class Training(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    participants = models.ManyToManyField(
        "BackendTennis.User",
        related_name="trainings"
    )
    unregisteredParticipants = fields.ArrayField(models.CharField(max_length=255), blank=True, default=list)
    cancel = models.BooleanField(default=False)
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            "id": self.id,
            "name": self.name,
            "participants": self.participants,
            "unregisteredParticipants": self.unregisteredParticipants,
            "cancel": self.cancel,
            "start": self.start,
            "end": self.end,
            "createAt": self.createAt,
            "updateAt": self.updateAt
        }
        return "%s" % to_return

    class Meta:
        app_label = "BackendTennis"
