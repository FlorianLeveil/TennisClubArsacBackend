# Generated by Django 4.1.7 on 2024-11-08 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackendTennis', '0033_sponsor_order_alter_navigationitem_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='year_experience',
            field=models.CharField(max_length=25),
        ),
    ]
