# Generated by Django 5.0.1 on 2024-02-22 22:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0006_alter_photo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]
