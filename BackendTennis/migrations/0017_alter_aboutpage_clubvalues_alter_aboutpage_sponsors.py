# Generated by Django 4.1.7 on 2024-10-28 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackendTennis', '0016_aboutpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutpage',
            name='clubValues',
            field=models.ManyToManyField(blank=True, related_name='about_pages', to='BackendTennis.clubvalue'),
        ),
        migrations.AlterField(
            model_name='aboutpage',
            name='sponsors',
            field=models.ManyToManyField(blank=True, related_name='about_pages', to='BackendTennis.sponsor'),
        ),
    ]
