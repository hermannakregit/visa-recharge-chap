from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from user.models import Fiche


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1','password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ClientForm(ModelForm):
    class Meta:
        model = Fiche
        fields = [
            'first_name',
            'last_name',
            'contact_one',
            'contact_two',
            'email',
            'birth',
            'birth_place',
            'identity',
            'identity_num',
            'identity_card_recto',
            'identity_card_verso',
            'country',
            'city',
            'address'
        ]

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})