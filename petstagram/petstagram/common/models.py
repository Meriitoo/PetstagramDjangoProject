from django.contrib.auth import get_user_model

from django.db import models

from petstagram.photos.models import Photo

UserModel = get_user_model()


class PhotoComment(models.Model):
    MAX_TEXT_LENGTH = 300
    text = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        null=False,
        blank=False,
    )

    publication_date_and_time = models.DateField(
        auto_now_add=True,
        blank=True,
        null=False,
    )

    photo = models.ForeignKey(
        Photo,
        on_delete=models.RESTRICT,
        null=False,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )


class PhotoLike(models.Model):
    #Photo's field for likes is named {NAME_OF_THIS_MODEL.lower(}_set
    photo = models.ForeignKey(
        Photo,
        on_delete=models.RESTRICT,
        null=False,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )

    # CASCADE - delete 1 photo and delete all connected comments
    # RESTRICT/PROTECT - delete 1 photo ONLY if no connected comments
    # SET_NULL - delete 1 photo, set null for FK at comments, null=True
    # SET_DEFAULT
