# Generated by Django 4.1.7 on 2024-10-30 15:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('BackendTennis', '0031_pricingpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricingpage',
            name='pricing',
            field=models.ManyToManyField(related_name='pricing_pages', to='BackendTennis.pricing'),
        ),
    ]
