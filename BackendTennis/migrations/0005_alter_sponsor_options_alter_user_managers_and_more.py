# Generated by Django 4.1.7 on 2024-09-13 13:28

import BackendTennis.models.UserManager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackendTennis', '0004_alter_booking_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sponsor',
            options={'ordering': ['createAt']},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', BackendTennis.models.UserManager.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]