from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model, login
from django.shortcuts import render

from petstagram.accounts.forms import UserCreateForm
from petstagram.photos.models import Photo

# Always get the model with get_user_model()
UserModel = get_user_model()


# def login_user(request):
#     return render(request, 'accounts/login-page.html')

# def register_user(request):
#     return render(request, 'accounts/register-page.html')
#
# def details_user(request, pk):
#     return render(request, 'accounts/profile-details-page.html')

# def edit_user(request, pk):
#     return render(request, 'accounts/profile-edit-page.html')
#

# def delete_user(request, pk):
#     return render(request, 'accounts/profile-delete-page.html')
#

class SignInView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'


class SignUpView(views.CreateView):
    template_name = 'accounts/register-page.html'
    form_class = UserCreateForm  # we can give model, but also we can give form for result
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Loging after registration
        login(request, self.object)

        return response


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')


class UserDetailsView(views.DetailView):
    template_name = 'accounts/profile-details-page.html'
    model = UserModel
    photos_paginate_by = 2

    def get_photos_page(self):
        return self.request.GET.get('page', 1)

    def get_paginated_photos(self):
        page = self.get_photos_page()
        photos = self.object.photo_set.order_by('-publication_date')  # for newest publications to show in profile

        paginator = Paginator(photos, self.photos_paginate_by)
        return paginator.get_page(page)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # when we have relation
        context['is_owner'] = self.request.user == self.object
        # self.object selected by primary key
        # self.request.user who is logged
        context['pets_count'] = self.object.pet_set.count()

        photos = self.object.photo_set \
            .prefetch_related(
            'photolike_set')  # for getting photos where userid is 1, ang give the photo with foreign key in other table, not all photos with that user
        # N + 1 query problem!!!!!!!!!!!!!!!!!!!!

        # In one request not two
        # Photo.objects.select_related() #taking objects with foreign key to current object, the opposite of prefetch with these Many-To-One, Many-To-Many
        # Photo.objects.prefetch_related() #take all photos prepare related things by foreign key, for all photos their photo like before, Many-To-One, Many-To-Many

        context['photos_count'] = photos.count()
        context['likes_count'] = sum(x.photolike_set.count() for x in photos)  # all photos with user id

        context['photos'] = self.get_paginated_photos()
        context['pets'] = self.object.pet_set.all()

        return context


class UserEditView(views.UpdateView):
    template_name = 'accounts/profile-edit-page.html'
    model = UserModel
    fields = ('first_name', 'last_name', 'gender', 'email',)

    def get_success_url(self):
        return reverse_lazy('details user', kwargs={
            'pk': self.request.user.pk,
        })


class UserDeleteView(views.DeleteView):
    template_name = 'accounts/profile-delete-page.html'
    model = UserModel
    success_url = reverse_lazy('index')
