from django.db import models

from BackendTennis.models.base_model.BaseMember import BaseMember


class Professor(BaseMember):
    image = models.ForeignKey(
        'BackendTennis.Image',
        on_delete=models.SET_NULL,
        related_name='professors',
        null=True
    )
    diploma = models.CharField(max_length=1000)
    year_experience = models.PositiveSmallIntegerField(default=0)
    best_rank = models.CharField(max_length=25)

    def __str__(self):
        to_return = {
            'id': self.id,
            'fullName': self.fullName,
            'role': self.role,
            'image': self.image,
            'order': self.order,
            'diploma': self.diploma,
            'year_experience': self.year_experience,
            'best_rank': self.best_rank,
            'createAt': self.createAt,
            'updateAt': self.updateAt,
        }
        return '%s' % to_return

    class Meta:
        ordering = ['order']
        app_label = 'BackendTennis'