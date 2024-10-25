# import uuid
#
# from django.db import models
#
# from BackendTennis.models import Professor, TeamMember
#
#
# class AboutPage(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     clubTitle = models.CharField(max_length=255)
#     clubDescription = models.TextField()
#     valueTitle = models.CharField(max_length=255)
#     sponsorTitle = models.CharField(max_length=255)
#
#     teamMembers = models.ManyToManyField(TeamMember, related_name='team_pages')
#     createAt = models.DateTimeField(auto_now_add=True)
#     updateAt = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         to_return = {
#             'id': self.id,
#             'professorsTitle': self.professorsTitle,
#             'professorsDescription': self.professorsDescription,
#             'professors': self.professors,
#             'teamMembersTitle': self.teamMembersTitle,
#             'teamMembers': self.teamMembers,
#             'dataCounter': self.dataCounter,
#             'createAt': self.createAt,
#             'updateAt': self.updateAt,
#         }
#         return '%s' % to_return
#
#     class Meta:
#         app_label = 'BackendTennis'
