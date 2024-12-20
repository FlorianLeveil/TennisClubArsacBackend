# Generated by Django 4.1.7 on 2024-10-24 15:53

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('BackendTennis', '0012_alter_teammember_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fullName', models.CharField(max_length=255, unique=True)),
                ('role', models.CharField(max_length=255)),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('diploma', models.CharField(max_length=1000)),
                ('year_experience', models.PositiveSmallIntegerField(default=0)),
                ('best_rank', models.CharField(max_length=25)),
                ('image',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='professors',
                                   to='BackendTennis.image')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
