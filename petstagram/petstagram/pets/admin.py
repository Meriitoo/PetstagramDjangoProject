from django.contrib import admin

from petstagram.pets.models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    #admin, have auto-genereted slug, can change the slug
    #users can't change the slug, auto-generated
    pass