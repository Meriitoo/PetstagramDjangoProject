from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import pyperclip
from django.urls import reverse

from petstagram.common.forms import PhotoCommentForm, SearchPhotosForm
from petstagram.common.models import PhotoLike
from petstagram.common.utils import get_photo_url
from petstagram.core.photo_utils import apply_likes_count, apply_user_liked_photo
from petstagram.photos.models import Photo


def index(request):
    search_form = SearchPhotosForm(request.GET)
    search_pattern = None

    if search_form.is_valid():
        search_pattern = search_form.cleaned_data['pet_name']

    # if search_form.is_valid(): # to see the info, clean data we see search form
    #     print('Data:')
    #     print(search_form.cleaned_data)
    # else:
    #     print('Error')
    #     print(search_form.errors)

    photos = Photo.objects.all()
    if search_pattern:
        photos = photos.filter(tagged_pets__name__icontains=search_pattern)  # i for case insensitive

    photos = [apply_likes_count(photo) for photo in photos]
    photos = [apply_user_liked_photo(photo) for photo in photos]
    print(photos)

    context = {
        'photos': photos,
        'comment_form': PhotoCommentForm(),
        'search_form': search_form,
    }

    return render(
        request,
        'common/home-page.html',
        context,
    )


@login_required
def like_photo(request, photo_id):
    user_liked_photos = PhotoLike.objects \
        .filter(photo_id=photo_id, user_id=request.user.pk) #just fon one like

    if user_liked_photos:
        user_liked_photos.delete()
    else:
        PhotoLike.objects.create(
            photo_id=photo_id,
            user_id=request.user.pk,
        )

    # # Variant 1
    # photo_like = PhotoLike(
    #     photo_id=photo_id,
    # )
    # photo_like.save()

    # # Variant 2
    # PhotoLike.objects.create(
    #     photo_id=photo_id,
    # )

    # # Variant 3 (wrong - additional call to db)
    # # Correct, only if validation is needed
    #
    # photo = Photo.objects.get(pk=photo_id)
    # PhotoLike.objects.create(
    #     photo=photo,
    # )

    return redirect(get_photo_url(request, photo_id))

    # returning the index of the photo
    # http://127.0.0.1:8000/#photo--3


def share_photo(request, photo_id):
    photo_details_url = reverse('details photo', kwargs={'pk': photo_id})
    pyperclip.copy(photo_details_url)
    return redirect(get_photo_url(request, photo_id))

    # http://127.0.0.1:8000/share/1/


def comment_photo(request, photo_id):
    photo = Photo.objects.filter(pk=photo_id).get()

    form = PhotoCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)  # Does not persist to DB  -> save the photo without save it into db
        comment.photo = photo  # set the photo
        comment.save()  # save it into db

    return redirect('index')
