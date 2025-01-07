from django import forms
from . models import Gender, User
from django.contrib.auth.forms import UserCreationForm


# User creation form

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password1', 'password2']


    def clean_username(self):
        # Auto Generate username from name
        name = self.cleaned_data.get('name')
        username = name.lower().replace(" ", "")
        return username
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Your Email'
        self.fields['phone'].widget.attrs['placeholder'] = 'Your Phone'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].widget.attrs['id'] = 'password_id1'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        self.fields['password2'].widget.attrs['id'] = 'password_id2'
