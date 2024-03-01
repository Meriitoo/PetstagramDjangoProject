from django.contrib.auth import get_user_model
from django.core.validators import URLValidator
from django.db import models
from django.utils.text import slugify

from petstagram.core.model_mixin import StrFromFieldMixin

UserModel = get_user_model()


class Pet(StrFromFieldMixin, models.Model):
    str_fields = ('id', 'name', 'slug')
    PET_MAX_NAME = 40
    name = models.CharField(
        max_length=PET_MAX_NAME,
        null=False,
        blank=False,
    )

    personal_photo = models.URLField(
        null=False,
        blank=False,
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True  # can't be empty if is it True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )

    # Pet().save() method when we create an object, and we can save or update in db

    def save(self, *args, **kwargs):
        # Create/Update
        super().save(*args, **kwargs)  # we adding this to generate id when we create some pet with blank True

        if not self.slug:  # this line is the slug to not change when we chnage the name
            self.slug = slugify(f'{self.id}-{self.name}')  # unique slug, id is none, when it is in db, id is not none

        # Without the 'if'
        # The url is /pets/4-stamat
        # Rename stamat to stamata
        # The new url is /pets/4-stamata, /pets/4-stamat does not work in other places, when it is defined

        # Update
        return super().save(*args, **kwargs)

# when we finish we do migration after we set up our postgre.db
