# Generated by Django 4.1.7 on 2024-10-30 09:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('BackendTennis', '0027_navigationbar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='navigationbar',
            name='title',
        ),
    ]
