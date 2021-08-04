from django import forms
from django.forms import fields
from .models import Profile


class ProfileForm(forms.Form):
    username = forms.CharField(max_length=100)
    avatar = forms.ImageField()

    def clean_avatar():
        pass