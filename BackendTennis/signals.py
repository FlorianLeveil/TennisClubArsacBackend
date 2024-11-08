import logging

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver

from BackendTennis.models import Render, NavigationItem, AboutPage, Sponsor, ClubValue, Professor, TeamPage, TeamMember

logger = logging.getLogger('BackendTennis.SIGNALS')


def _log_function_start_info(sender, instance):
    logger.debug(f'[ {sender.__name__} ] Running update pre-saver asked by : {instance.id}')


@receiver(pre_save, sender=Render)
def validate_navigation_items_on_render_update(sender, instance, **kwargs):
    _log_function_start_info(sender, instance)
    related_navigation_items = NavigationItem.objects.filter(navBarRender__id=instance.id)
    for nav_item in related_navigation_items:
        try:
            nav_item.save(navBarRender=instance)
        except ValidationError as e:
            raise e


@receiver(m2m_changed, sender=AboutPage.sponsors.through)
def validate_sponsor_order(sender, instance, action, **kwargs):
    _log_function_start_info(sender, instance)
    if action == 'post_add':
        sponsor_ids = kwargs.get('pk_set', [])
        sponsors = Sponsor.objects.filter(id__in=sponsor_ids)
        for sponsor in sponsors:
            try:
                sponsor.validate_unique_order(instance, sponsor.brandName, instance.clubTitle)
            except ValidationError as e:
                raise e


@receiver(m2m_changed, sender=AboutPage.clubValues.through)
def validate_club_values_order(sender, instance, action, **kwargs):
    _log_function_start_info(sender, instance)
    if action == 'post_add':
        club_value_ids = kwargs.get('pk_set', [])
        club_values = ClubValue.objects.filter(id__in=club_value_ids)
        for club_value in club_values:
            try:
                club_value.validate_unique_order(instance, club_value.title, instance.clubTitle)
            except ValidationError as e:
                raise e


@receiver(m2m_changed, sender=TeamPage.professors.through)
def validate_professors_order(sender, instance, action, **kwargs):
    _log_function_start_info(sender, instance)
    if action == 'post_add':
        professors_id = kwargs.get('pk_set', [])
        professors = Professor.objects.filter(id__in=professors_id)
        for professor in professors:
            try:
                professor.validate_unique_order(instance, professor.fullName, instance.professorsTitle)
            except ValidationError as e:
                raise e


@receiver(m2m_changed, sender=TeamPage.teamMembers.through)
def validate_team_members_order(sender, instance, action, **kwargs):
    _log_function_start_info(sender, instance)
    if action == 'post_add':
        team_members_id = kwargs.get('pk_set', [])
        team_members = TeamMember.objects.filter(id__in=team_members_id)
        for team_member in team_members:
            try:
                team_member.validate_unique_order(instance, team_member.fullName, instance.teamMembersTitle)
            except ValidationError as e:
                raise e
