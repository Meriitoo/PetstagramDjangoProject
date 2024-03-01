# 'ModelForm' and 'Form'
# -'ModelForm' binds to models
# -'Form' is detached from models
from django import forms

from petstagram.core.form_mixin import DisabledFormMixin
from petstagram.pets.models import Pet


class PetBaseForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['name'].widget.attrs['placeholder'] = 'Pet name'

    class Meta:
        model = Pet
        # fields = '__all__' #(not the case, we want to skip slug)
        fields = ('name', 'date_of_birth', 'personal_photo')
        # exclude = ('slug',)
        labels = {
            'name': 'Pet name',
            'personal_photo': 'Link to Image',
            'date_of_birth': 'Date of Birth',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Pet name'
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'placeholder': 'mm/dd/yyyy',
                    'type': 'date'
                }
            ),
            'personal_photo': forms.URLInput(
                attrs={
                    'placeholder': 'Link to image'
                }
            )
        }


class PetCreateForm(PetBaseForm):
    pass


class PetEditForm(DisabledFormMixin, PetBaseForm):
    disabled_fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disable_fields()


class PetDeleteForm(DisabledFormMixin,PetBaseForm):
    # for data to can't edit them, to be disabled
    disabled_fields = ('name', 'date_of_birth', 'personal_photo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disable_fields()

    def save(self, commit=True):
        # overriding save method, because when we save we can't delete it
        if commit:  # send to database
            self.instance.delete()
        else:
            pass

        return self.instance

