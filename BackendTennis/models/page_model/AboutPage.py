import uuid

from django.db import models

from BackendTennis.models import Image, ClubValue, Sponsor


class AboutPage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clubTitle = models.CharField(max_length=255, null=True, blank=True)
    clubDescription = models.TextField(null=True, blank=True)
    clubImage = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name='about_pages',
        null=True,
        blank=True
    )
    dataCounter = models.JSONField(default=list, null=True, blank=True)

    clubValueTitle = models.CharField(max_length=255, null=True, blank=True)
    clubValues = models.ManyToManyField(
        ClubValue,
        related_name='about_pages',
        blank=True
    )

    sponsorTitle = models.CharField(max_length=255, null=True, blank=True)
    sponsors = models.ManyToManyField(
        Sponsor,
        related_name='about_pages',
        blank=True
    )

    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        to_return = {
            'id': self.id,
            'clubTitle': self.clubTitle,
            'clubDescription': self.clubDescription,
            'clubImage': self.clubImage,
            'dataCounter': self.dataCounter,
            'valueTitle': self.clubValueTitle,
            'clubValues': self.clubValues,
            'sponsorTitle': self.sponsorTitle,
            'sponsors': self.sponsors,
            'createAt': self.createAt,
            'updateAt': self.updateAt,
        }
        return '%s' % to_return

    class Meta:
        app_label = 'BackendTennis'
