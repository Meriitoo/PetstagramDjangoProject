from django.urls import path, include

from petstagram.photos.views import add_photo, edit_photo, details_photo, delete_photo

urlpatterns = (
    path('add/', add_photo, name='add photo'),
    path('<int:pk>/', include([
        path('', details_photo, name='details photo'),
        path('edit/', edit_photo, name='edit photo'),
        path('delete/', delete_photo, name='delete photo')
    ])),

# http://127.0.0.1:8000/photos/add/

# http://127.0.0.1:8000/photos/1/
# http://127.0.0.1:8000/photos/1/edit/


)