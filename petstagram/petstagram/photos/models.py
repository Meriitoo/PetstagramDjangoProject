from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from petstagram.core.model_mixin import StrFromFieldMixin
from petstagram.pets.models import Pet
from petstagram.photos.validators import validate_image_less_han_5mb


# pip install pillow for imagesfield

UserModel = get_user_model()


class Photo(StrFromFieldMixin, models.Model):
    str_fields = ('pk', 'photo', 'location')
    MIN_DESCRIPTION_LENGTH = 10
    MAX_DESCRIPTION_LENGTH = 300

    MAX_LOCATION_LENGTH = 30

    # Requires mediafiles to wrok correctly
    photo = models.ImageField(
        upload_to='pet_photos/',
        #http://127.0.0.1:8000/media/pet_photos/dog.jpg
        null=False,
        blank=True,
        validators=(validate_image_less_han_5mb,) #they are callable
    )
    # uplouding images in filesystem, just saving the path and saving it in database

    description = models.CharField(
        # DB validation
        max_length=MAX_DESCRIPTION_LENGTH,

        validators=(
            # Django/python validation, not DB validation
            MinLengthValidator(MIN_DESCRIPTION_LENGTH),
        ),
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=MAX_LOCATION_LENGTH,
        null=True,
        blank=True,
    )

    publication_date = models.DateField(
        # Automatically sets current date on 'save' (update or create)
        auto_now=True,  # auto_now_add = when we created it for first time
        null=False,
        blank=True,
    )

    # One-to-one relations
    # One-to-many relations

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )

    # Many-to-many relations
    tagged_pets = models.ManyToManyField(
        Pet,  # models photos go to another app models pets, photos can't work without pets
        blank=True,
    )
