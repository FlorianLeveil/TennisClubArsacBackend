# Generated by Django 4.1.7 on 2024-10-25 14:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('BackendTennis', '0014_alter_teammember_description_teampage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubValue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('updateAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['createAt'],
            },
        ),
    ]