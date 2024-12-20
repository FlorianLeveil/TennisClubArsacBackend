# Generated by Django 4.1.7 on 2024-11-08 16:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('BackendTennis', '0034_alter_professor_year_experience'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammember',
            name='fullName',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='image',
        ),
        migrations.AddField(
            model_name='teammember',
            name='fullNames',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='teammember',
            name='images',
            field=models.ManyToManyField(related_name='team_members', to='BackendTennis.image'),
        ),
    ]
