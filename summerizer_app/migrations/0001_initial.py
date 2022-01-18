# Generated by Django 4.0.1 on 2022-01-13 01:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feeback',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('IP', models.CharField(max_length=255)),
                ('feedback', models.CharField(max_length=255)),
            ],
        ),
    ]
