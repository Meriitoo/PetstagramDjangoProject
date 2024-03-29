# Generated by Django 5.0.1 on 2024-02-01 15:33

import petstagram.photos.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_alter_photo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(blank=True, upload_to='mediafiles/pet_photos/', validators=[petstagram.photos.validators.validate_image_less_han_5mb]),
        ),
    ]
