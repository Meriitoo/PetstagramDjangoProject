from django.urls import path, include

from petstagram.pets.views import add_pet, details_pet, edit_pet, delete_pet

urlpatterns = (
    path('add/', add_pet, name='add pet'),
    path('<str:username>/pet/<slug:pet_slug>/', include([
        path('', details_pet, name='details pet'),
        path('edit/', edit_pet, name='edit pet'),
        path('delete/', delete_pet, name='delete pet'),
    ])),

# http://127.0.0.1:8000/pets/dpncho/pet/gosho/ - slug for nothing
# http://127.0.0.1:8000/pets/dpncho/pet/gosho/edit/ - slug for edit
)