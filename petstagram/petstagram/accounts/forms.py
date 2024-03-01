from django.contrib.auth import forms as auth_forms, get_user_model
from django.contrib.auth.forms import UsernameField

UserModel = get_user_model()


class UserEditForm(auth_forms.UserChangeForm):
    class Meta:
        model = UserModel
        fields = "__all__"
        field_classes = {'username': auth_forms.UsernameField}


class UserCreateForm(auth_forms.UserCreationForm):
    # placeholders = {
    #     'username': 'Username'
    # }
    # 

    # override the meta
    class Meta:
        model = UserModel
        fields = ('username', 'email')
        field_classes = {'username': auth_forms.UsernameField}

