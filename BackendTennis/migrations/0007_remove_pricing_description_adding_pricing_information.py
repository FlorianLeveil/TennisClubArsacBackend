# Generated by Django 4.1.7 on 2024-10-22 10:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('BackendTennis', '0006_alter_pricing_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricing',
            name='description',
        ),
        migrations.AddField(
            model_name='pricing',
            name='license',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pricing',
            name='site_access',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pricing',
            name='extra_data',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='pricing',
            name='information',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
