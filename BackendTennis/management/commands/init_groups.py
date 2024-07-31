from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from BackendTennis.models import Image


class Command(BaseCommand):
    help = 'Initialise groups and permissions for the Image module'

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name='Image')
        content_type = ContentType.objects.get_for_model(Image)

        # Create permissions
        add_perm = Permission.objects.create(codename='add_image', name='Can add images', content_type=content_type)
        change_perm = Permission.objects.create(codename='change_image', name='Can change images',
                                                content_type=content_type)
        delete_perm = Permission.objects.create(codename='delete_image', name='Can delete images',
                                                content_type=content_type)
        view_perm = Permission.objects.create(codename='view_image', name='Can view images', content_type=content_type)

        # Add permissions to group
        group.permissions.add(add_perm, change_perm, delete_perm, view_perm)

        self.stdout.write(self.style.SUCCESS('Successfully created group and permissions for images'))
