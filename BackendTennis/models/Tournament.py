from django.db import models

from BackendTennis.models.BaseActivity import BaseActivity


class Tournament(BaseActivity):
    participants = models.ManyToManyField(
        "BackendTennis.User",
        related_name="tournaments"
    )

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
