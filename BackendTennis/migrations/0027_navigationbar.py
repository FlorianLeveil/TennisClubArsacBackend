# Generated by Django 4.1.7 on 2024-10-30 08:04

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('BackendTennis', '0026_remove_navigationitem_order_navigationitem_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavigationBar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, null=True)),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('logo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           related_name='navigation_bars', to='BackendTennis.image')),
                ('navigationItems',
                 models.ManyToManyField(related_name='navigation_bars', to='BackendTennis.navigationitem')),
                ('routeLogo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                related_name='navigation_bars', to='BackendTennis.route')),
            ],
        ),
    ]